#!/bin/bash

echo "Gemini Video Analyzer を起動します..."

# Python仮想環境のセットアップと有効化
if [ ! -d ".venv" ]; then
    echo "Python仮想環境をセットアップしています..."
    python3 -m venv .venv
fi

if [ -f ".venv/bin/activate" ]; then
    echo "仮想環境を有効化します。"
    source .venv/bin/activate
else
    echo "エラー: 仮想環境のセットアップに失敗しました。"
    exit 1
fi

# 必要なライブラリのインストール（初回または更新時）
echo "必要なライブラリをインストールしています..."
pip3 install -r requirements.txt

# .envファイルの確認
if [ ! -f ".env" ]; then
    if [ -f "env.example" ]; then
        echo "警告: .envファイルが見つかりません。env.exampleをコピーします。"
        cp env.example .env
        echo "重要: .envファイルにAPIキーを設定してください。"
    else
        echo "エラー: env.exampleファイルが見つかりません。"
        exit 1
    fi
fi

# 必要なディレクトリの作成
mkdir -p videos_to_analyze analysis_reports

# Webアプリケーションの起動
echo "Webアプリケーションを起動しています..."
python3 app.py

echo
echo "アプリケーションが終了しました。"
