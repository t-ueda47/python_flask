"""お問い合わせフォームの作成(入力チェック追加)"""

import logging
from email_validator import validate_email, EmailNotValidError
from flask import Flask, redirect, render_template, request, url_for, flash

app = Flask(__name__)

# flash使用のためSECRET_KEYの設定
app.config["SECRET_KEY"] = "samplekey123"
# ログの設定
app.logger.setLevel(logging.DEBUG)


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
        # TODOメールを送る（最後に実装）
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

        # メールを送るTODO

        # 問い合わせ完了エンドポイントへリダイレクトする
        flash("問い合わせありがとうございます。")

        return redirect(url_for("contact_complete"))

    # 【G: Get】リダイレクトされてきたら、完了画面（HTML）を表示する
    return render_template("contact_complete.html")


if __name__ == "__main__":
    app.run(debug=True)
