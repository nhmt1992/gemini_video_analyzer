import requests
import logging

def update_progress(step: str, progress: int, message: str = None):
    """
    進捗状況をWebアプリケーションに送信する
    """
    try:
        data = {
            'step': step,
            'progress': progress,
            'message': message or ''
        }
        requests.post('http://localhost:5000/update_progress', json=data)
    except Exception as e:
        logging.error(f"進捗状況の更新中にエラーが発生しました: {e}")