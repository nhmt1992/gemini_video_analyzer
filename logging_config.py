import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler

def setup_logging():
    # ログディレクトリの作成
    log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
    os.makedirs(log_dir, exist_ok=True)

    # ログファイル名に日付を含める
    log_filename = os.path.join(log_dir, f'app_{datetime.now().strftime("%Y%m%d")}.log')

    # ロガーの設定
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # ファイルハンドラの設定（ローテーション付き）
    file_handler = RotatingFileHandler(
        log_filename,
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.INFO)
    file_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
    )
    file_handler.setFormatter(file_formatter)

    # コンソールハンドラの設定
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(console_formatter)

    # ハンドラの追加（重複登録防止）
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    # 起動メッセージ
    logging.info('=== KRONOS Video Analyzer ログシステム初期化完了 ===')