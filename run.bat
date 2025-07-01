@echo off
setlocal enabledelayedexpansion

echo === KRONOS Video Analyzer ===
echo 起動準備を開始します...

:: Pythonのインストール確認
python --version >nul 2>&1
if errorlevel 1 (
    echo エラー: Pythonがインストールされていません。
    echo https://www.python.org/downloads/ からPython 3.9以上をインストールしてください。
    pause
    exit /b 1
)

:: 仮想環境の確認と作成
if not exist .venv (
    echo 仮想環境を作成しています...
    python -m venv .venv
    if errorlevel 1 (
        echo エラー: 仮想環境の作成に失敗しました。
        pause
        exit /b 1
    )
)

:: 仮想環境の有効化
call .venv\Scripts\activate
if errorlevel 1 (
    echo エラー: 仮想環境の有効化に失敗しました。
    pause
    exit /b 1
)

:: 依存パッケージのインストール確認と実行
pip show flask >nul 2>&1
if errorlevel 1 (
    echo 必要なパッケージをインストールしています...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo エラー: パッケージのインストールに失敗しました。
        pause
        exit /b 1
    )
)

:: ディレクトリの作成
if not exist videos_to_analyze mkdir videos_to_analyze
if not exist analysis_reports mkdir analysis_reports
if not exist logs mkdir logs

:: .envファイルの確認
if not exist .env (
    echo .envファイルが見つかりません。
    echo env.exampleをコピーして.envを作成し、APIキーを設定してください。
    copy env.example .env
    notepad .env
    echo .envファイルを編集し、APIキーを設定してから再度実行してください。
    pause
    exit /b 1
)

:: アプリケーションの実行
echo 全ての準備が完了しました。アプリケーションを起動します...
start http://localhost:5000
python app.py

endlocal

