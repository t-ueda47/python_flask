"""Flaskのミニマムアプリケーション"""

from flask import Flask, render_template, url_for

# Flaskクラスをインスタンス化する
app = Flask(__name__)


# URLと実行する関数をマッピングする
@app.route("/")
def index():
    """トップページを表示する関数"""
    # templates/index.html を呼び出して表示する
    return render_template("index.html")


@app.route("/hello/<name>")
def hello(name):
    """追加されたルーティング"""
    return f"こんにちは,{name}！！"


# show_nameエンドポイントを作成する
@app.route("/name/<name>")
def show_name(name):
    """変数をテンプレートエンジンに渡す"""
    return render_template("index.html", name=name)


# 条件分岐ifの実験
@app.route("/profile")
def profile():
    """プロフィールページを表示する関数"""

    user_data = {"is_logged_in": True}  # 例：ログイン中
    return render_template("index.html", user=user_data)


# 繰り返し（for文）
@app.route("/show_articles")
def show_articles():
    """辞書データをfor文で表示させる関数"""

    # テンプレートに渡す記事データのリスト（辞書のリスト形式）
    article_list = [
        {"id": 1, "title": "Flaskの基本を学ぼう", "date": "2026-09-01"},
        {"id": 2, "title": "Jinja2テンプレートの使い方", "date": "2026-09-05"},
        {"id": 3, "title": "Webクリエイター試験対策", "date": "2026-09-10"},
    ]

    # index.html を呼び出し、HTML側の 'articles' にデータを渡す
    return render_template("index.html", articles=article_list)


# 繰り返し処理が生み出す「詳細ページ用の処理」
@app.route("/article/<int:article_id>")
def article_detail(article_id):
    """リンクをクリックした時に生成する内容"""

    return f"記事 ID: {article_id} の詳細ページです"


# ターミナルでの実験用
with app.test_request_context():
    print(url_for("article_detail", article_id=100))
    print(url_for("hello", name="ueda"))
    print(url_for("index"))
    print(url_for("profile"))
    print(url_for("show_articles"))
    print(url_for("show_name", name="mizuno"))
