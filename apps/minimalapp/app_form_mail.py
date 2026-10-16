"""問い合わせフォームの内容でメール送信(テンプレートメール送信対応)"""

import logging
import os
import smtplib
from email_validator import EmailNotValidError, validate_email
from flask import Flask, flash, redirect, render_template, request, url_for
from flask_mail import Mail, Message

app = Flask(__name__)

# flash使用のためSECRET_KEYの設定
app.config["SECRET_KEY"] = "samplekey123"
# ログの設定
app.logger.setLevel(logging.DEBUG)

# --- メール設定（.envから取得してコンフィグにセット） ---
app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER")
app.config["MAIL_PORT"] = int(os.environ.get("MAIL_PORT"))
app.config["MAIL_USE_TLS"] = os.environ.get("MAIL_USE_TLS") == "True"
app.config["MAIL_USE_SSL"] = os.environ.get("MAIL_USE_SSL") == "True"
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.environ.get("MAIL_DEFAULT_SENDER")

# Flask-Mail の初期化
mail = Mail(app)


# メール送信関数
def send_email(to, subject, template, **kwargs):
    """メールを送信する関数"""
    msg = Message(subject, recipients=[to])
    msg.body = render_template(template + ".txt", **kwargs)
    msg.html = render_template(template + ".html", **kwargs)
    mail.send(msg)


@app.route("/")
def index():
    """トップページにアクセスされたら/contactへ転送する"""
    return redirect(url_for("contact"))


@app.route("/contact")
def contact():
    """入力画面を表示する処理 (GET専用)"""

    # お問い合わせの入力フォーム（HTML）を表示する
    return render_template("contact.html")


@app.route("/contact/complete", methods=["GET", "POST"])
def contact_complete():
    """フォーム送信処理 & 完了画面表示（PRGパターンの核）"""

    # 【P: Post】データ受取＆処理
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        description = request.form["description"]

        # 入力チェック
        is_valid = True
        if not username:
            flash("ユーザ名は必須です")
            is_valid = False

        if not email:
            flash("メールアドレスは必須です")
            is_valid = False

        # メールアドレスの形式になっていなければ例外発生
        try:
            validate_email(email)
        except EmailNotValidError:
            flash("メールアドレスの形式で入力してください")
            is_valid = False
            # ログ1
            app.logger.warning("メールアドレス形式エラー : %s", email)

        # 問い合わせがnullだったら
        if not description:
            flash("問い合わせ内容は必須です")
            is_valid = False

        # バリデーションクリアしなかった
        if not is_valid:
            # ログ2
            app.logger.warning("入力チェックエラーが発生しました")

            return redirect(url_for("contact"))

        # ログ3
        app.logger.info("お問い合わせ受付完了")

        # TODO箇所の埋め込み：メール送信メソッドへ
        try:
            send_email(
                email,
                "問い合わせありがとうございました。",
                "contact_mail",
                username=username,
                description=description,
            )
            app.logger.info("メール送信成功: %s", email)
        except smtplib.SMTPException as e:
            app.logger.error("メール送信失敗: %s", e)
            flash("メール送信に失敗しました。")
            return redirect(url_for("contact"))

        # 完了フラッシュメッセージをセットし、GETへリダイレクト（PRGの「R」）
        flash(
            "お問い合わせ内容はメールにて送信しました。お問い合わせありがとうございました。"
        )
        return redirect(url_for("contact_complete"))

    # リダイレクトされて来たらWeb用完了画面（contact_complete.html）を表示（PRGの「G」）
    return render_template("contact_complete.html")


if __name__ == "__main__":
    app.run(debug=True)
