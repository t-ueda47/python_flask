"""セッションを使ったサンプルコード（ステップ3段階）"""

from datetime import timedelta
import os
import uuid
from dotenv import load_dotenv
from flask import Flask, render_template, request, session
from markupsafe import escape

# .env ファイルの読み込み
load_dotenv()

# Flaskアプリのインスタンス作成
app = Flask(__name__)

# .env から秘密鍵を取得して app にセット
app.secret_key = os.environ.get("FLASK_SECRET_KEY")

# セッションの有効期限設定（例: 7日間）
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=7)

# グローバル変数としてセッションストアを定義
SESSION_STORE = {}


@app.route("/", methods=["GET", "POST"])
def login():
    """【ステップ3】ログインページの表示 ＆ ログイン処理"""

    # POSTリクエスト（フォーム送信時）の処理
    if request.method == "POST":
        # 1. フォームから値を取り出す（前後の余計な空白を strip() で除去）
        user_id = request.form.get("user_id", "").strip()
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()

        if user_id and username and email:
            # 2. サーバー側で一意なランダム文字列（セッションID）を生成
            session_id = str(uuid.uuid4())

            # 3. サーバーの金庫（SESSION_STORE）にデータを登録
            SESSION_STORE[session_id] = {
                "user_id": escape(user_id),
                "username": escape(username),
                "email": escape(email),
            }

            # 4. ブラウザの Cookie には「セッションID」のみを書き込む
            session["session_id"] = session_id
            session.permanent = True

            # 動作確認用ログ（ターミナルでSESSION_STOREの中身を確認）
            print("\n--- サーバー側の SESSION_STORE ---")
            print(SESSION_STORE)
            print("-----------------------------------\n")

    # GETリクエスト時、およびPOST処理後にログイン画面を表示
    return render_template("session_home.html")


if __name__ == "__main__":
    app.run(debug=True)