"""アプリケーションコンテキストとリクエストコンテキスト"""

from flask import Flask, current_app, request

app = Flask(__name__)

"""
アプリケーションコンテキストにデータを入れる
（アプリ起動時に、設定値としてセット）
"""
app.config["STORE_NAME"] = "Pythonカフェ"


@app.route("/")
def index():
    """
    2つのコンテキストからデータを取り出して使う
    （アクセスが来たら、それぞれの引き出しから取る）
    """

    # --- アプリケーションコンテキストを使う ---
    # アプリ全体の設定用の引き出しからデータを取り出す
    store = current_app.config["STORE_NAME"]

    # --- リクエストコンテキストを使う ---
    # ブラウザから送られてきた「1回ごとのアクセス情報」の引き出しから取り出す
    user_agent = request.headers.get("User-Agent")  # アクセスに使ったブラウザの種類
    user_ip = request.remote_addr  # アクセスしてきた人のIPアドレス
    method = request.method  # GET や POST などの通信方法

    return f"""
    <h1>{store} へようこそ！</h1>
    <hr>
    <h3>【リクエストコンテキストから取得したデータ】</h3>
    <ul>
        <li><b>あなたのIPアドレス:</b> {user_ip}</li>
        <li><b>アクセス方法:</b> {method}</li>
        <li><b>利用ブラウザ:</b> {user_agent}</li>
    </ul>
    """


if __name__ == "__main__":
    app.run(debug=True)
