"""メールを送信する"""

import os
import smtplib
from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)

# --- .env から値を取り出してコンフィグにセット ---
app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER")
app.config["MAIL_PORT"] = int(os.environ.get("MAIL_PORT"))
app.config["MAIL_USE_TLS"] = os.environ.get("MAIL_USE_TLS") == "True"
app.config["MAIL_USE_SSL"] = os.environ.get("MAIL_USE_SSL") == "True"
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.environ.get("MAIL_USERNAME")

# Flask-Mail の初期化
mail = Mail(app)


@app.route("/")
def send_mail():
    """メールを送信する"""

    msg = Message(
        subject="【テスト】自動送信メール",
        recipients=["k-ueda@obmps.com"],
        body="これは .env の設定を使用して送信されたメールです。",
    )

    try:
        mail.send(msg)
        return "メールの送信に成功しました！"
    except smtplib.SMTPException as e:
        return f"送信失敗: {e}"


if __name__ == "__main__":
    app.run(debug=True)
