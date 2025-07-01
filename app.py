from flask import Flask, render_template, request, redirect, url_for, jsonify, send_from_directory
from flask_socketio import SocketIO
from flask_cors import CORS
import os
import subprocess
import configparser
import logging
import sys
import shutil
import webbrowser

# ロギング設定
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 1024  # 1GB max-size
app.config['UPLOAD_FOLDER'] = 'videos_to_analyze'
ALLOWED_EXTENSIONS = {'mp4', 'mov', 'avi'}

CORS(app)
socketio = SocketIO(app, async_mode='threading', cors_allowed_origins="*", ping_timeout=60)

# config.iniのパス
CONFIG_FILE_PATH = "config.ini"

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE_PATH, encoding='utf-8')
    goal = config.get('VideoAnalysis', 'goal', fallback='')
    target_audience = config.get('VideoAnalysis', 'target_audience', fallback='')
    issue = config.get('VideoAnalysis', 'issue', fallback='')
    return render_template('index.html', goal=goal, target_audience=target_audience, issue=issue)

@app.route('/update_progress', methods=['POST'])
def update_progress():
    """進捗状況の更新を受け取り、WebSocketで送信する"""
    try:
        data = request.get_json()
        logging.info(f"進捗更新を受信: {data}")
        
        # 進捗情報をクライアントに送信
        socketio.emit('progress_update', data)
        
        return jsonify({'status': 'success'})
    except Exception as e:
        logging.error(f"進捗更新中にエラーが発生: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        if 'video' not in request.files:
            return jsonify({'status': 'error', 'message': '動画ファイルがアップロードされていません'}), 400
        
        file = request.files['video']
        if file.filename == '':
            return jsonify({'status': 'error', 'message': 'ファイルが選択されていません'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'status': 'error', 'message': '許可されていないファイル形式です'}), 400

        # アップロードフォルダの作成
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])

        # ファイル名を安全に保存
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        goal = request.form['goal']
        target_audience = request.form['target_audience']
        issue = request.form['issue']

        # config.iniを更新
        config = configparser.ConfigParser()
        config.read(CONFIG_FILE_PATH, encoding='utf-8')
        if not config.has_section('VideoAnalysis'):
            config.add_section('VideoAnalysis')
        config.set('VideoAnalysis', 'goal', goal)
        config.set('VideoAnalysis', 'target_audience', target_audience)
        config.set('VideoAnalysis', 'issue', issue)

        with open(CONFIG_FILE_PATH, 'w', encoding='utf-8') as configfile:
            config.write(configfile)
        logging.info("config.iniを更新しました。")

        # 分析プロセスを開始
        python_executable = os.path.join(os.path.dirname(sys.executable), "python.exe")
        process = subprocess.Popen(
            [python_executable, "main.py"],
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
        logging.info("main.pyの分析プロセスを開始しました。")
        
        # 初期進捗状況を送信
        socketio.emit('progress_update', {
            'step': '動画ファイルの処理準備',
            'progress': 0,
            'message': '処理を開始しています...'
        })
        
        return jsonify({'status': 'success'})
        
    except Exception as e:
        logging.error(f"分析プロセスの開始中にエラーが発生: {e}")
        socketio.emit('analysis_error', {
            'message': f'エラーが発生しました: {str(e)}'
        })
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/reports/<path:filename>')
def serve_report(filename):
    """レポートファイルを提供する"""
    return send_from_directory('analysis_reports', filename)

@socketio.on('connect')
def handle_connect():
    """クライアント接続時の処理"""
    logging.info('クライアントが接続しました')

@socketio.on('disconnect')
def handle_disconnect():
    """クライアント切断時の処理"""
    logging.info('クライアントが切断しました')

if __name__ == '__main__':
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)