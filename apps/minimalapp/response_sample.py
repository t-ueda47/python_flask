"""レスポンスのサンプルコード"""

from datetime import timedelta
import os
import uuid
from dotenv import load_dotenv
from flask import (
    Flask,
    redirect,
    render_template,
    request,
    session,
    url_for,
    make_response,
)
from markupsafe import escape

# .env ファイルの読み込み
load_dotenv()

# Flaskアプリのインスタンス作成
app = Flask(__name__)

# 秘密鍵の設定
app.secret_key = os.environ.get("FLASK_SECRET_KEY")

# セッションの有効期限設定（7日間）
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=7)

# サーバー側のデータ保存領域（金庫）
SESSION_STORE = {}


@app.route("/")
@app.route("/session_home")
def session_home():
    """
    マイページ表示（ユーザー情報の復元・取得）
    """
    # Cookie（ブラウザ）から session_id（文字列）を取り出す
    session_id = session.get("session_id")
    user_info = None

    # session_id が存在し、かつサーバーの SESSION_STORE に登録されているか確認
    if session_id and session_id in SESSION_STORE:
        # 金庫から対応するユーザー情報を取得
        user_info = SESSION_STORE[session_id]

    # user_info をテンプレートに渡して描画
    return render_template("session_home.html", user_info=user_info)


@app.route("/login", methods=["POST"])
def login():
    """ログイン処理（セッションIDの発行と保存）"""
    user_id = request.form.get("user_id", "").strip()
    username = request.form.get("username", "").strip()
    email = request.form.get("email", "").strip()

    if user_id and username and email:
        # 一意なセッションID（UUID）を生成
        session_id = str(uuid.uuid4())

        # サーバー側の SESSION_STORE に登録
        SESSION_STORE[session_id] = {
            "user_id": escape(user_id),
            "username": escape(username),
            "email": escape(email),
        }

        # Cookie には session_id だけを保存
        session["session_id"] = session_id
        session.permanent = True

    # ログイン完了後、マイページ（session_home）へリダイレクト
    return redirect(url_for("session_home"))


@app.route("/logout")
def logout():
    """
    【ステップ5】ログアウト処理
    1. Cookie から session_id を取得
    2. SESSION_STORE（インメモリDB）から該当データを削除
    3. Cookie から session_id を削除（破棄）
    """
    # Cookie（ブラウザ）から session_id を取り出す
    session_id = session.get("session_id")

    # SESSION_STORE（インメモリDB）から該当のセッションデータを削除
    if session_id and session_id in SESSION_STORE:
        SESSION_STORE.pop(session_id, None)

    # Cookie（セッション）から session_id を削除
    session.pop("session_id", None)

    # ログアウト完了後、マイページ（未ログイン状態の画面）へリダイレクト
    return redirect(url_for("session_home"))


@app.route("/contact", methods=["GET", "POST"])
def contact():
    """レスポンスのテスト"""

    # 1. 表示する本文を準備
    response_body = (
        "<h1>お問い合わせページ</h1><p>レスポンスオブジェクトの実験中です。</p>"
    )

    # 2. status_code を設定してレスポンスオブジェクトを作成
    response = make_response(response_body, 200)

    # 3. headers の追加
    response.headers["Content-Type"] = "text/html; charset=utf-8"
    response.headers["X-Custom-Header"] = "Experiment-Value"

    # 4. set_cookie の設定
    response.set_cookie(key="user_mode", value="visitor", max_age=3600)

    # 5. delete_cookie の実行
    if "user_mode" in request.cookies:
        response.delete_cookie("user_mode")

    return response


if __name__ == "__main__":
    app.run(debug=True)
