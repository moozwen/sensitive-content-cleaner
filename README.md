# Sensitive Content Cleaner

テキストファイル内の機密情報を検出し、匿名化するための Python ツールです。Microsoft Presidio を使用して、個人情報や機密データを自動的に検出し、安全に匿名化します。

## 機能

- 日本語テキスト内の機密情報を高精度で検出
- 検出された情報を自動的に匿名化
- カスタム認識器による特定の情報パターンの検出
  - 電話番号（一般・内線）
  - メールアドレス
  - クレジットカード番号
  - 金額表記
  - その他カスタム定義可能なパターン
- 特定の単語やフレーズを検出から除外する機能

## 環境構築

### 前提条件

- Python 3.11 以上
- Poetry（Python パッケージ管理ツール）

### Poetry の環境構築

```bash
poetry install
```

### spaCy のインストール

```bash
poetry run python -m spacy download ja_core_news_trf
# 日本語モデルのダウンロード
poetry add https://github.com/explosion/spacy-models/releases/download/ja_core_news_sm-3.8.0/ja_core_news_sm-3.8.0.tar.gz
```

## 使用方法

### 実行前の準備

- `data` ディレクトリに除去したい文言を含むテキストファイルを配置します

### 実行

```bash
# 初回は時間がかかります
poetry run python -m sensitive_content_cleaner.main data/sample_text.txt
```

デフォルトでは、匿名化されたテキストは `./data/anonymized_text.txt` に出力されます。
出力先を変更する場合は、以下のように指定します：

```bash
poetry run python -m sensitive_content_cleaner.main data/sample_text.txt --output_path ./data/output.txt
```

## 検出可能な情報

このツールは以下の種類の情報を検出・匿名化できます：

1. **基本的な個人情報**

   - 氏名
   - メールアドレス
   - 電話番号（固定電話、携帯電話）
   - 住所

2. **業務関連情報**

   - 内線番号
   - 金額表記
   - クレジットカード番号
   - 銀行口座情報

3. **カスタム定義情報**
   - 特定の会社名や製品コードなどを検出から除外

## カスタマイズ

認識器のカスタマイズは `src/sensitive_content_cleaner/recognizer/` ディレクトリ内のファイルを編集することで行えます：

- `custom_recognizers.py`: カスタム認識器の定義
- `localized_predefined_recognizers.py`: 既存の認識器の日本語対応版

新しい認識パターンを追加する場合は、`custom_recognizers.py` に新しい関数を追加し、`presidio_engine.py` の `__init__` メソッド内で登録してください。
