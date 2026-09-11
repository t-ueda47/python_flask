"""Flaskのミニマムアプリケーション"""

from flask import Flask

# Flaskクラスをインスタンス化する
app = Flask(__name__)


# URLと実行する関数をマッピングする
@app.route("/")
def index():
    """トップページを表示する関数"""
    return "Hello, Flaskbook!"


@app.route("/hello")
def hello():
    """追加されたルーティング"""
    return "こんにちは！！"
