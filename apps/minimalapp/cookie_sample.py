"""クッキーを利用したサンプルコード"""

from flask import (
    Flask,
    flash,
    make_response,
    redirect,
    render_template,
    request,
    url_for,
)

# Flaskクラスをインスタンス化する
app = Flask(__name__)

# flashメッセージ用に必要（簡略化した書き方）
app.secret_key = "samplekey123"


@app.route("/")
def index():
    """トップページにアクセスされたら/contactへ転送する"""
    return redirect(url_for("contact"))


# 問い合わせフォーム画面 (GET)
@app.route("/contact", methods=["GET"])
def contact():
    """Cookieから値を受け取り、HTMLに渡す"""
    # クッキーから保存されている値を取得（無ければ空文字）
    username = request.cookies.get("username", "")
    email = request.cookies.get("email", "")

    # テンプレートに渡して表示。
    return render_template(
        # username=username:左: HTML側の変数名 = 右: Python側の変数名
        "contact.html",
        username=username,
        email=email,
        description="",
    )


@app.route("/contact/complete", methods=["POST"])
def contact_complete():
    """送信処理 (POST) -> 送信完了画面へのリダイレクト"""

    # フォームデータの取得
    username = request.form.get("username", "")
    email = request.form.get("email", "")
    description = request.form.get("description", "")

    # 簡易入力チェック（空送信の場合）
    if not username or not email or not description:
        flash("すべての項目を入力してください")
        # エラー時は入力途中の値を持たせてフォームに戻す
        return render_template(
            "contact.html",
            username=username,
            email=email,
            description=description,
        )
    # --- ToDOメール送信処理 (send_email など) をここで実行 ---

    # 完了画面へのリダイレクトレスポンスを作成7
    response = make_response(redirect(url_for("contact_complete_page")))

    # 次回用にユーザー名とメールアドレスをクッキーに保存（例: 30日間有効）
    # ※ description（本文）は毎回違うためクッキーには保存しません
    response.set_cookie("username", username, max_age=60 * 60 * 24 * 30)
    response.set_cookie("email", email, max_age=60 * 60 * 24 * 30)

    return response


@app.route("/contact/complete", methods=["GET"])
def contact_complete_page():
    """送信完了画面 (GET)"""

    return render_template("contact_complete.html")


# 今開いている（アクティブな）Pythonファイルを実行
if __name__ == "__main__":
    app.run(debug=True)
