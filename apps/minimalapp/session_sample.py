"""セッションを使ったサンプルコード"""

from datetime import timedelta
from flask import Flask, redirect, render_template, request, session, url_for

app = Flask(__name__)

# セッションの暗号化に必要な秘密鍵（必須）
app.secret_key = "secret_key_sample_123"

# セッションの有効期限を「7日間」に設定
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=7)


@app.route("/")
def session_home():
    """セッションの取得と表示（ホーム画面）"""
    # session.get("キー名") で値を取得（未保存の場合は None が返る）
    username = session.get("username")

    # session_home.html に取得した username を渡して描画
    return render_template("session_home.html", username=username)


@app.route("/login", methods=["POST"])
def login():
    """セッションのセット（ログイン処理）"""
    # フォームからの入力値を取得
    user_input = request.form.get("username", "")

    if user_input:
        # 【セッションのセット】辞書形式で保存
        session["username"] = user_input

        # 有効期限（7日間）を有効化
        session.permanent = True

    # 処理完了後は session_home 関数（トップ画面）へリダイレクト
    return redirect(url_for("session_home"))


@app.route("/logout")
def logout():
    """セッションの削除（ログアウト処理）"""

    # 【セッションの削除】指定したキーのデータを削除
    session.pop("username", None)

    # ログアウト後も session_home 関数（トップ画面）へリダイレクト
    return redirect(url_for("session_home"))


# 今開いている（アクティブな）Pythonファイルを実行
if __name__ == "__main__":
    app.run(debug=True)
