## 1.LINE Notify でトークン払い出し
- [LINE Notify](https://notify-bot.line.me/ja/)にアクセス
- 登録サービス管理からサービスを登録するとトークンが払い出されるのでメモする

## 2.必要パッケージのインストール
```python
envファイル読み込み必要なのでインストール
pip install python-dotenv
```

## 3.env ファイルの設定
- LINE_TOKEN：払い出したトークンを入力
- MONITOR_SITE：複数サイト監視する場合は,で区切る
- SSL_EXPIRY_DAYS：SSL証明書を監視する期間(30であれば30日を切ったらアラートを上げる)

必要に応じてcronとかに登録して実行する。
(アラート結果はmonitoring.logに出力される)
