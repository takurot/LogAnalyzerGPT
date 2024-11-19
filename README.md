# LogAnalyzerGPT

LogAnalyzerGPTは、Linuxシステムのログを収集・解析し、エラーや不審な活動を特定して要約します。OpenAIのGPT-4モデルを利用して、システム状態の概要を生成します。要約結果はテキストファイルとして保存されます。

## 特徴
- **ログ収集**: `/var/log`ディレクトリ内の主要なログファイルを収集。
- **エラー抽出**: `error`, `failed`, `critical`などのキーワードを使用してエラーや警告を抽出。
- **要約生成**: OpenAIのAPIを利用してログの要約を生成。
- **ファイル保存**: 生成した要約を`log_summary.txt`として保存。

---

## 必要条件
- Python 3.7以上
- OpenAI APIキー
- Linuxシステムログへの読み取りアクセス権
- Pythonライブラリ:
  - `openai`

### 依存関係のインストール
必要なライブラリをインストールするには以下を実行してください:
```bash
pip install openai
```

---

## 使用方法

### 1. リポジトリをクローン
```bash
git clone https://github.com/your_username/LogAnalyzerGPT.git
cd LogAnalyzerGPT
```

### 2. OpenAI APIキーの設定
環境変数にAPIキーを設定してください `export OPENAI_API_KEY=your_api_key`

### 3. スクリプトの実行
スクリプトを実行するには、`sudo`権限で以下を実行します:
```bash
python3 log_analyzer_gpt.py
```

### 4. 出力結果の確認
- 実行後、カレントディレクトリに`log_summary.txt`という名前のファイルが生成されます。
- ファイルには、GPTによるログの要約結果が保存されています。

---

## ログ解析の仕組み

1. **ログ収集**:
   以下の主要なログファイルからデータを収集します（存在する場合のみ）:
   - `/var/log/syslog`
   - `/var/log/messages`
   - `/var/log/dmesg`
   - `/var/log/auth.log`

2. **エラーフィルタリング**:
   キーワード（例: `error`, `failed`, `critical`など）を基に、重要なログ行のみを抽出します。

3. **ChatGPTを使用した要約**:
   OpenAIのGPT-4モデルにフィルタリングされたログを送信し、システム状態の要約を取得します。

4. **要約結果の保存**:
   要約結果を`log_summary.txt`として保存します。

---

## 注意事項

- スクリプトを実行する際は、ログファイルへの読み取りアクセス権を確認してください。
- OpenAI APIの利用には料金が発生する場合があります。
- 大量のログを送信すると、APIリクエストサイズ制限を超える可能性があります。

---

## 今後の改善点

- ログファイルの指定をコマンドライン引数でカスタマイズ可能にする。
- ログ解析後のアラート通知機能を追加。

---

## ライセンス
このプロジェクトはMITライセンスのもとで提供されています。