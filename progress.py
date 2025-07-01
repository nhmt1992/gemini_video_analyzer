import requests
import logging
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class ProgressStatus:
    step: str
    progress: int
    message: str
    started_at: datetime
    completed_at: Optional[datetime] = None
    error: Optional[str] = None

class ProgressTracker:
    def __init__(self):
        self._current_status = None
        self._history = []
        self._error = None

    def start_step(self, step: str, message: str = "") -> None:
        """新しいステップを開始"""
        self._current_status = ProgressStatus(
            step=step,
            progress=0,
            message=message,
            started_at=datetime.now()
        )
        self._history.append(self._current_status)
        logging.info(f"ステップ開始: {step} - {message}")

    def update_progress(self, progress: int, message: str = "") -> None:
        """進捗状況を更新"""
        if self._current_status:
            self._current_status.progress = progress
            if message:
                self._current_status.message = message
            logging.info(f"進捗更新: {progress}% - {message}")

    def complete_step(self, message: str = "") -> None:
        """現在のステップを完了としてマーク"""
        if self._current_status:
            self._current_status.progress = 100
            self._current_status.completed_at = datetime.now()
            if message:
                self._current_status.message = message
            logging.info(f"ステップ完了: {self._current_status.step} - {message}")

    def set_error(self, error: str) -> None:
        """エラー状態を設定"""
        self._error = error
        if self._current_status:
            self._current_status.error = error
        logging.error(f"エラーが発生: {error}")

    def get_current_status(self) -> dict:
        """現在の状態を取得"""
        if not self._current_status:
            return {
                'step': 'アイドル状態',
                'progress': 0,
                'message': '処理待機中...'
            }
        
        return {
            'step': self._current_status.step,
            'progress': self._current_status.progress,
            'message': self._current_status.message,
            'error': self._current_status.error
        }

    def get_history(self) -> list:
        """進捗履歴を取得"""
        return [
            {
                'step': status.step,
                'progress': status.progress,
                'message': status.message,
                'started_at': status.started_at.isoformat(),
                'completed_at': status.completed_at.isoformat() if status.completed_at else None,
                'error': status.error
            }
            for status in self._history
        ]

    def reset(self) -> None:
        """進捗状況をリセット"""
        self._current_status = None
        self._history.clear()
        self._error = None
        logging.info("進捗状況をリセットしました")