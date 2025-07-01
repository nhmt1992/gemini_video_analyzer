# KRONOS 動画分析アプリ - 取扱説明書
# KRONOS Video Analysis App - User Manual

# KRONOS Video Analyzer

ショート動画（TikTok、YouTube Shorts等）の分析と改善を支援するAIツール

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

[English documentation below | 英語版は下部にあります](#english)

## 概要

KRONOS Video Analyzerは、ショート動画のクリエイターを支援するためのAIパワードツールです。
アップロードされた動画を分析し、視聴維持率やエンゲージメントを向上させるための具体的な改善案を提案します。

### 主な機能

- 🎥 動画の自動分析
- 📊 詳細な改善レポート生成
- 🎯 視聴者心理に基づく改善提案
- 📝 具体的な改善脚本の提案
- 🌐 ブラウザベースのUI

## クイックスタート

```bash
# リポジトリのクローン
git clone https://github.com/yourusername/gemini_video_analyzer.git
cd gemini_video_analyzer

# Pythonの仮想環境を作成（推奨）
python -m venv .venv
source .venv/bin/activate  # Unix系
# または
.venv\Scripts\activate     # Windows

# 依存パッケージのインストール
pip install -r requirements.txt

# 環境変数の設定
cp env.example .env
# .envファイルを編集してAPIキーを設定

# アプリケーションの起動
python app.py  # または run.bat/run.sh
```

## 詳細なセットアップガイド

### 必要な環境

- Python 3.9以上
- モダンなWebブラウザ（Microsoft Edge推奨）
- Google AI Studio APIキー

### 1. Python 3 のインストール
お使いのPCにPythonがインストールされていない場合、以下の手順で設定してください：

1. [Python公式サイト](https://www.python.org/downloads/)から最新版のPython 3をダウンロード
   - Windows: 「Windows installer (64-bit)」を選択
   - macOS: 「macOS 64-bit universal2 installer」を選択
2. ダウンロードしたインストーラーを実行
3. **重要:** インストール時に「Add Python to PATH」のチェックボックスを必ずオンにする
4. インストールが完了したら、コマンドプロンプト（またはターミナル）を開いて以下のコマンドを実行し、インストールを確認：
   ```
   python --version
   ```

### 2. アプリケーションのダウンロードと展開
1. アプリケーションのZIPファイルをダウンロード
2. ダウンロードしたZIPファイルを任意の場所に展開
   - 推奨: デスクトップまたはドキュメントフォルダ
   - 注意: パスに日本語が含まれていても問題ありません

### 3. 必要なライブラリのインストール
このアプリが動作するために必要なライブラリをインストールします。

#### Windows:
1. `run.bat` をダブルクリック（初回起動時に自動でインストール開始）
2. もし自動インストールが失敗する場合は、コマンドプロンプトを管理者として実行し、以下のコマンドを順に実行：
   ```
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

#### macOS:
1. 「ターミナル」アプリを開く
2. 以下のコマンドを順に実行：
   ```
   cd アプリケーションの展開先パス
   python3 -m pip install --upgrade pip
   pip3 install -r requirements.txt
   ```

### 4. Google AI Studio APIキーの取得と設定
1. [Google AI Studio](https://makersuite.google.com/app/apikey)にアクセス
2. Googleアカウントでログイン
3. 「APIキーを作成」をクリック
4. 生成されたAPIキーをコピー
5. フォルダ内の `env.example` ファイルをコピーして `.env` という名前で保存
6. `.env` ファイルをメモ帳で開き、`"YOUR_API_KEY"` を実際のAPIキーに置き換えて保存

**例:**
```
GOOGLE_API_KEY="AIzaSyXXXXXXXXXXXXXXXXXXX"
```
**注意：`.env`ファイルと、そこに含まれるAPIキーは、絶対に他人に教えたり、公開したりしないでください。**

---

## アプリの使い方

初回設定が終われば、使い方はとても簡単です。

### 1. 動画を準備する
動画ファイルを分析用フォルダに配置する方法は2通りあります：

#### A. 手動で配置する場合（推奨）
- フォルダ内にある `videos_to_analyze` フォルダを開きます。
- 分析したい動画ファイル（MP4など）を、このフォルダの中に入れます。
- ファイルサイズ制限: 1件あたり1GB以下

#### B. Webブラウザから直接アップロードする場合
- Microsoft Edge（推奨）: 
  - ドラッグ＆ドロップでアップロード可能
  - ファイル選択ボタンでの選択も可能
- Google Chrome: 
  - ドラッグ＆ドロップは非対応
  - ファイル選択ボタンでの選択のみ可能
- その他のブラウザ: 
  - 基本機能のみ対応
  - Microsoft Edgeの使用を推奨
- ファイルサイズ制限: 1件あたり1GB以下

### 2. アプリを実行する
- **Windows:** 
  1. `run.bat` ファイルをダブルクリック
  2. ブラウザが自動で開き、アプリケーションが起動
  3. もしブラウザが開かない場合は、手動で `http://localhost:5000` にアクセス

- **macOS:**
  1. （初回のみ）`run.sh` ファイルを右クリック > 「情報を見る」 > 「このアプリケーションで開く」で「ターミナル」を選択
  2. `run.sh` ファイルをダブルクリック
  3. ブラウザが自動で開き、アプリケーションが起動
  4. もしブラウザが開かない場合は、手動で `http://localhost:5000` にアクセス
  - 注意: 実行できない場合は、ターミナルで以下のコマンドを実行して実行権限を付与
    ```
    chmod +x run.sh
    ```

### 3. 結果を確認する
- 分析が完了すると、`analysis_reports` フォルダが自動で作成されます。
- 分析結果のHTMLレポートが自動でブラウザに表示されます。
- すべてのレポートは `analysis_reports` フォルダにも保存されます。
- レポートは標準的なWebブラウザで閲覧可能です。

## 既知の制限事項
- Google Chromeでのドラッグ＆ドロップによるファイルアップロードは現在対応していません。
- 動画ファイルのサイズ制限：1件あたり1GB以下
- 対応動画形式：MP4, MOV, AVI
- 処理時間の目安：
  - 1分以内の動画：約2-3分
  - 1-3分の動画：約3-5分
  - 3分以上の動画：5分以上

## トラブルシューティング

### アプリが起動しない場合
1. Pythonが正しくインストールされているか確認：
   ```
   python --version   # Windows
   python3 --version  # macOS
   ```
2. 必要なライブラリが正しくインストールされているか確認：
   ```
   pip list | findstr flask            # Windows
   pip3 list | grep google-generativeai  # macOS
   ```
3. `.env`ファイルが正しく設定されているか確認
4. ポート5000が他のアプリケーションで使用されていないか確認

### 分析が開始されない場合
1. `videos_to_analyze`フォルダに動画ファイルが正しく配置されているか確認
2. 動画ファイルの形式がMP4、MOV、またはAVIであるか確認
3. ファイルサイズが1GB以下であるか確認
4. インターネット接続が正常であるか確認
5. APIキーが有効であるか確認

### レポートが生成されない場合
1. `analysis_reports`フォルダが存在するか確認
2. ディスクの空き容量が十分あるか確認（1GB以上推奨）
3. アプリケーションの実行権限が適切か確認

---

何か問題があれば、開発者にお知らせください。

---

<a name="english"></a>
# KRONOS Video Analyzer

An AI-powered tool for analyzing and improving short-form videos (TikTok, YouTube Shorts, etc.)

## Overview

KRONOS Video Analyzer is an AI-powered tool designed to assist short-form video creators. 
It analyzes uploaded videos and provides specific improvement suggestions to enhance viewer retention and engagement.

### Key Features

- 🎥 Automated video analysis
- 📊 Detailed improvement reports
- 🎯 Viewer psychology-based suggestions
- 📝 Concrete script improvements
- 🌐 Browser-based UI

## Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/gemini_video_analyzer.git
cd gemini_video_analyzer

# Create Python virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # Unix-like
# or
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp env.example .env
# Edit .env file to set your API key

# Start the application
python app.py  # or run.bat/run.sh
```

## Detailed Setup Guide

### Required Environment

- Python 3.9 or higher
- Modern web browser (Microsoft Edge recommended)
- Google AI Studio API key

### 1. Install Python 3
If Python is not installed on your PC, follow these steps:

1. Download the latest Python 3 from [Python Official Website](https://www.python.org/downloads/)
   - Windows: Select "Windows installer (64-bit)"
   - macOS: Select "macOS 64-bit universal2 installer"
2. Run the downloaded installer
3. **Important:** Make sure to check "Add Python to PATH" during installation
4. After installation, open Command Prompt (or Terminal) and verify the installation:
   ```
   python --version
   ```

### 2. Download and Extract the Application
1. Download the ZIP file of the application
2. Extract the downloaded ZIP file to a desired location
   - Recommended: Desktop or Documents folder
   - Note: It is okay if the path contains Japanese characters

### 3. Install Required Libraries
Install the necessary libraries for this app to function.

#### Windows:
1. Double-click `run.bat` (automatic installation starts on first launch)
2. If automatic installation fails, run Command Prompt as administrator and execute:
   ```
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

#### macOS:
1. Open Terminal app
2. Execute the following commands:
   ```
   cd path/to/extracted_application
   python3 -m pip install --upgrade pip
   pip3 install -r requirements.txt
   ```

### 4. Get and Configure Google AI Studio API Key
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Log in with your Google account
3. Click "Create API Key"
4. Copy the generated API key
5. Copy `env.example` file in the folder and save as `.env`
6. Open `.env` with Notepad and replace `"YOUR_API_KEY"` with your actual API key

**Example:**
```
GOOGLE_API_KEY="AIzaSyXXXXXXXXXXXXXXXXXXX"
```
**Note: Never share or publish your `.env` file and the API key it contains.**

---

## How to Use the App

Once the initial setup is complete, using the app is very simple.

### 1. Prepare Your Video
There are two ways to place video files for analysis:

#### A. Manual Placement (Recommended)
- Open the `videos_to_analyze` folder
- Place your video file (MP4, etc.) in this folder
- File size limit: Up to 1GB per file

#### B. Direct Upload via Web Browser
- Microsoft Edge (Recommended): 
  - Supports drag & drop upload
  - File selection button is also available
- Google Chrome: 
  - Drag & drop is not supported
  - File selection button only
- Other browsers: 
  - Basic functionality only
  - Microsoft Edge is recommended
- File size limit: Up to 1GB per file

### 2. Run the App
- **Windows:** 
  1. Double-click the `run.bat` file
  2. The browser should open automatically, and the application will start
  3. If the browser doesn't open, manually access `http://localhost:5000`

- **macOS:**
  1. (First time only) Right-click `run.sh` > "Get Info" > "Open with" select "Terminal"
  2. Double-click the `run.sh` file
  3. The browser should open automatically, and the application will start
  4. If the browser doesn't open, manually access `http://localhost:5000`
  - Note: If it doesn't run, enter the following command in Terminal to grant execution permission
    ```
    chmod +x run.sh
    ```

### 3. Check Results
- Upon completion, an `analysis_reports` folder is automatically created
- The analysis report in HTML format opens automatically in your browser
- All reports are also saved in the `analysis_reports` folder
- Reports can be viewed in standard web browsers

## 開発者向け情報

### アーキテクチャ

- **Frontend**: HTML/CSS/JavaScript + WebSocket
- **Backend**: Flask + Flask-SocketIO
- **AI**: Google Gemini Pro API

### プロジェクト構造

```
gemini_video_analyzer/
├── app.py              # メインアプリケーション（Flaskサーバー）
├── main.py            # 動画分析エンジン
├── progress.py        # 進捗状況管理
├── requirements.txt   # 依存パッケージ
├── prompts/          # プロンプトテンプレート
├── templates/        # HTMLテンプレート
├── videos_to_analyze/ # 分析対象の動画保存先
└── analysis_reports/ # 生成されたレポートの保存先
```

### 貢献方法

1. このリポジトリをFork
2. 新しいブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m 'Add amazing feature'`)
4. ブランチをPush (`git push origin feature/amazing-feature`)
5. Pull Requestを作成

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。詳細は[LICENSE](LICENSE)をご覧ください。

## 謝辞

- [Google Gemini Pro API](https://deepmind.google/technologies/gemini/)
- [Flask](https://flask.palletsprojects.com/)
- コミュニティの皆様

---

何か問題があれば、開発者にお知らせください。