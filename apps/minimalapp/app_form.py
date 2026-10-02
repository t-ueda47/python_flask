"""お問い合わせフォームの作成"""

from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)


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

        # --- ターミナルに出力する処理 ---
        print(f"ユーザー名: {username}")
        print(f"メールアドレス: {email}")
        print(f"お問い合わせ内容: {description}")

        # contactエンドポイントへリダイレクトする
        return redirect(url_for("contact_complete"))

    # 【G: Get】リダイレクトされてきたら、完了画面（HTML）を表示する
    return render_template("contact_complete.html")


if __name__ == "__main__":
    app.run(debug=True)
