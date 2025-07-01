#!/bin/bash

echo "=== KRONOS Video Analyzer ==="
echo "起動準備を開始します..."

# Pythonのインストール確認
if ! command -v python3 &> /dev/null; then
    echo "エラー: Python 3がインストールされていません。"
    echo "https://www.python.org/downloads/ からPython 3.9以上をインストールしてください。"
    read -p "Enterキーを押して終了..."
    exit 1
fi

# 仮想環境の確認と作成
if [ ! -d ".venv" ]; then
    echo "仮想環境を作成しています..."
    python3 -m venv .venv
    if [ $? -ne 0 ]; then
        echo "エラー: 仮想環境の作成に失敗しました。"
        read -p "Enterキーを押して終了..."
        exit 1
    fi
fi

# 仮想環境の有効化
source .venv/bin/activate
if [ $? -ne 0 ]; then
    echo "エラー: 仮想環境の有効化に失敗しました。"
    read -p "Enterキーを押して終了..."
    exit 1
fi

# 依存パッケージのインストール確認と実行
if ! pip show flask &> /dev/null; then
    echo "必要なパッケージをインストールしています..."
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "エラー: パッケージのインストールに失敗しました。"
        read -p "Enterキーを押して終了..."
        exit 1
    fi
fi

# ディレクトリの作成
mkdir -p videos_to_analyze analysis_reports logs

# .envファイルの確認
if [ ! -f ".env" ]; then
    echo ".envファイルが見つかりません。"
    echo "env.exampleをコピーして.envを作成し、APIキーを設定してください。"
    cp env.example .env
    if command -v open &> /dev/null; then
        open -t .env
    else
        nano .env
    fi
    echo ".envファイルを編集し、APIキーを設定してから再度実行してください。"
    read -p "Enterキーを押して終了..."
    exit 1
fi

# ブラウザを開く
echo "全ての準備が完了しました。アプリケーションを起動します..."
sleep 2

if command -v open &> /dev/null; then
    open http://localhost:5000
elif command -v xdg-open &> /dev/null; then
    xdg-open http://localhost:5000
elif command -v firefox &> /dev/null; then
    firefox http://localhost:5000
fi

# アプリケーションの実行
python3 app.py
