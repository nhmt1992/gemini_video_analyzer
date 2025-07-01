import google.generativeai as genai
import os
import time
from dotenv import load_dotenv
import markdown
import sys
import requests
import logging
import configparser
from google.api_core.exceptions import GoogleAPIError
from progress import update_progress
import webbrowser

# --- 準備: 環境変数の読み込み ---
load_dotenv()

# --- ロギング設定 ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- 1. グローバル設定 ---
try:
    api_key = os.environ["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except KeyError:
    logging.error("エラー: .envファイルに 'GOOGLE_API_KEY' が設定されていません。")
    sys.exit(1)

VIDEO_FOLDER_PATH = os.getenv("VIDEO_FOLDER_PATH")
if not VIDEO_FOLDER_PATH:
    logging.error("エラー: .envファイルに 'VIDEO_FOLDER_PATH' が設定されていません。")
    sys.exit(1)

OUTPUT_HTML_DIR = "analysis_reports"

VIDEO_FILE_FORMATS = ('.mp4', '.mpeg', '.mov', '.avi', '.flv', '.mpg', '.webm', '.wmv', '.3gpp')

# --- 2. HTMLレポートのテンプレート (改行を意識したCSSに改良) ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TikTok動画分析レポート: {{ video_title }}</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji";
            line-height: 1.6;
            background-color: #f6f8fa;
            color: #24292e;
            margin: 0;
            padding: 20px;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background-color: #ffffff;
            border: 1px solid #d1d5da;
            border-radius: 6px;
            padding: 20px 40px;
        }
        h1, h2, h3, h4, h5, h6 {
            border-bottom: 1px solid #eaecef;
            padding-bottom: 0.3em;
            margin-top: 24px;
            margin-bottom: 16px;
            font-weight: 600;
        }
        h1 { font-size: 2em; }
        h2 { font-size: 1.5em; }
        h3 { font-size: 1.25em; }
        table {
            width: 100%;
            border-collapse: collapse;
            display: block;
            overflow-x: auto;
            margin-bottom: 20px;
        }
        th, td {
            border: 1px solid #dfe2e5;
            padding: 8px 12px;
            text-align: left;
            vertical-align: top;
        }
        th {
            background-color: #f6f8fa;
            font-weight: bold;
        }
        tr:nth-child(2n) {
            background-color: #f6f8fa;
        }
        code {
            font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, Courier, monospace;
            background-color: rgba(27,31,35,0.05);
            padding: .2em .4em;
            margin: 0;
            font-size: 85%;
            border-radius: 3px;
        }
        pre {
            background-color: #f6f8fa;
            border-radius: 3px;
            padding: 16px;
            overflow: auto;
            white-space: pre-wrap; /* この行が改行を保持します */
            word-wrap: break-word; /* この行が長い単語を折り返します */
        }
        pre > code {
            background-color: transparent; padding: 0; margin: 0; font-size: 100%; border: 0;
        }
        hr {
            border: 0; height: 1px; background-color: #d1d5da; margin: 24px 0;
        }
        ul, ol { padding-left: 20px; }
        li { margin-bottom: 0.5em; } /* リスト項目間のスペースを調整 */
    </style>
</head>
<body>
    <div class="container">
        <h1>TikTok動画分析レポート</h1>
        <h2>分析対象: <code>{{ video_title }}</code></h2>
        <hr>
        {{ content }}
    </div>
</body>
</html>
"""

# --- 3. プロンプト生成関数 (ご要望に合わせて改良) ---
PROMPT_FILE_PATH = "prompts/analysis_prompt.txt"

def load_prompt_template(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"エラー: プロンプトファイルが見つかりません: {file_path}")
        sys.exit(1)
    except IOError as e:
        print(f"エラー: プロンプトファイルの読み込み中にエラーが発生しました: {file_path} - {e}")
        sys.exit(1)

def get_analysis_prompt(goal, target_audience, issue):
    """
    ユーザーからの入力に基づいて、Geminiに渡す最終的なプロンプトを生成する。
    """
    prompt_template = load_prompt_template(PROMPT_FILE_PATH)
    return prompt_template.format(goal=goal, target_audience=target_audience, issue=issue)

# --- 4. ヘルパー関数 (変更なし) ---
def create_html_report(markdown_content: str, video_filename: str, output_dir: str):
    try:
        html_content = markdown.markdown(markdown_content, extensions=['markdown.extensions.tables'])
        report_html = HTML_TEMPLATE.replace("{{ video_title }}", video_filename)
        report_html = report_html.replace("{{ content }}", html_content)
        output_filename = os.path.splitext(video_filename)[0] + ".html"
        output_filepath = os.path.join(output_dir, output_filename)
        
        with open(output_filepath, "w", encoding="utf-8") as f:
            f.write(report_html)
        logging.info(f"HTMLレポートが正常に生成されました: {output_filepath}")
        
        # レポートをブラウザで開く
        webbrowser.open('file://' + os.path.abspath(output_filepath))
        
        return output_filepath
    except (IOError, OSError) as e:
        logging.error(f"HTMLレポートの書き込み中にエラーが発生しました: {e}")
    except Exception as e:
        logging.error(f"HTMLレポートの生成中に予期せぬエラーが発生しました: {e}")
    return None

# --- 5. メイン分析関数 (変更なし) ---
def analyze_video_from_path(video_path: str, prompt: str):
    uploaded_file = None
    video_filename = os.path.basename(video_path)
    print("-" * 50)
    logging.info(f"動画ファイル '{video_filename}' の処理を開始します。")
    try:
        # 進捗状況: ファイルのアップロード開始
        update_progress('ファイルのアップロード', 20, f"ファイルをアップロード中: {video_filename}")
        logging.info(f"ファイルをアップロード中: {video_path}")
        uploaded_file = genai.upload_file(path=video_path, display_name=video_filename)
        logging.info(f"アップロード完了。File Name: {uploaded_file.name}")
        
        # 進捗状況: サーバー側の処理待機
        update_progress('ファイルのアップロード', 40, "サーバー側でのファイル処理を待機しています...")
        logging.info("サーバー側でのファイル処理を待機しています...")
        while uploaded_file.state.name == "PROCESSING":
            time.sleep(10)
            uploaded_file = genai.get_file(name=uploaded_file.name)
            logging.info(f"現在の状態: {uploaded_file.state.name}")
        
        if uploaded_file.state.name != "ACTIVE":
            logging.error(f"ファイルの処理に失敗しました。状態: {uploaded_file.state.name}")
            return
        
        # 進捗状況: Geminiによる分析開始
        update_progress('Geminiによる分析', 60, "Geminiが動画を分析しています...")
        logging.info("ファイルの準備が完了しました。")
        logging.info("Geminiによる動画分析を開始します... (最大10分程度かかる場合があります)")
        model = genai.GenerativeModel(model_name="gemini-2.5-pro")
        response = model.generate_content([uploaded_file, prompt], request_options={"timeout": 600})
        
        # 進捗状況: レポート生成
        update_progress('レポート生成', 80, "分析結果をレポートに変換しています...")
        logging.info("\n--- 分析結果 (動画コンサルタント KRONOS より) ---")
        logging.info(response.text)
        logging.info("--- 分析終了 ---\n")
        create_html_report(response.text, video_filename, OUTPUT_HTML_DIR)
        
        # 進捗状況: 完了
        update_progress('レポート生成', 100, "分析が完了しました！")
        
    except GoogleAPIError as e:
        logging.error(f"Gemini APIとの通信中にエラーが発生しました: {e}")
        update_progress('エラー', 0, f"Gemini APIとの通信中にエラーが発生しました: {e}")
    except requests.exceptions.RequestException as e:
        logging.error(f"ネットワーク接続中にエラーが発生しました: {e}")
        update_progress('エラー', 0, f"ネットワーク接続中にエラーが発生しました: {e}")
    except Exception as e:
        logging.error(f"'{video_filename}' の処理中に予期せぬエラーが発生しました: {e}")
        update_progress('エラー', 0, f"予期せぬエラーが発生しました: {e}")
    finally:
        if uploaded_file:
            try:
                logging.info(f"アップロードされたファイル '{uploaded_file.name}' を削除します。")
                genai.delete_file(name=uploaded_file.name)
                logging.info("ファイルの削除が完了しました。")
            except Exception as e:
                logging.warning(f"ファイル '{uploaded_file.name}' の削除に失敗しました: {e}")
    print("-" * 50 + "\n")

# --- 6. メイン実行ブロック (変更なし) ---
if __name__ == "__main__":
    # 進捗状況: 設定の読み込み
    update_progress('設定の読み込み', 0, "設定ファイルを読み込んでいます...")
    
    # --- 設定ファイルの読み込み ---
    config = configparser.ConfigParser()
    config_file_path = "config.ini"
    if not os.path.exists(config_file_path):
        logging.error(f"エラー: 設定ファイル '{config_file_path}' が見つかりません。")
        update_progress('エラー', 0, f"設定ファイル '{config_file_path}' が見つかりません。")
        sys.exit(1)
    
    try:
        config.read(config_file_path, encoding='utf-8')
        goal = config.get('VideoAnalysis', 'goal', fallback='指定なし')
        target_audience = config.get('VideoAnalysis', 'target_audience', fallback='指定なし')
        issue = config.get('VideoAnalysis', 'issue', fallback='指定なし')
        logging.info(f"設定ファイルから以下の情報を読み込みました:\n  ゴール: {goal}\n  ターゲット視聴者像: {target_audience}\n  課題: {issue}")
    except configparser.Error as e:
        logging.error(f"エラー: 設定ファイル '{config_file_path}' の読み込み中にエラーが発生しました: {e}")
        sys.exit(1)

    if not os.path.isdir(VIDEO_FOLDER_PATH):
        logging.error(f"指定されたフォルダー '{VIDEO_FOLDER_PATH}' が存在しません。")
        sys.exit(1)
    os.makedirs(OUTPUT_HTML_DIR, exist_ok=True)

    video_files = [os.path.join(VIDEO_FOLDER_PATH, f) for f in os.listdir(VIDEO_FOLDER_PATH) if f.lower().endswith(VIDEO_FILE_FORMATS)]
    if not video_files:
        logging.info(f"フォルダー '{VIDEO_FOLDER_PATH}' に動画が見つかりませんでした。")
    else:
        logging.info(f"分析対象の動画が {len(video_files)} 件見つかりました。")
        for i, video_file in enumerate(video_files):
            logging.info(f"\n[{i+1}/{len(video_files)}] 次の動画の分析準備をします: {os.path.basename(video_file)}")
            # input() 関数を削除し、設定ファイルから読み込んだ値を使用
            final_prompt = get_analysis_prompt(goal, target_audience, issue)
            analyze_video_from_path(video_file, final_prompt)
        logging.info("🎉 すべての動画の分析が完了しました。")
        logging.info(f"レポートは '{OUTPUT_HTML_DIR}' フォルダに保存されています。")