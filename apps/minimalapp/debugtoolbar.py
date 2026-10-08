"""flask-debubtoobarを使用する"""

from flask import Flask

# ライブラリを読み込む
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

# SECRET_KEYの設定が必須（セキュリティのため）
app.config["SECRET_KEY"] = "samplekey123"

# デバッグモードをONにする（ツールバーを表示させるため）
app.debug = True

# リダイレクト時に画面を止めない設定（教科書の設定）
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

# アプリにツールバーを組み込む
toolbar = DebugToolbarExtension(app)


@app.route("/")
def hello():
    """HTMLとしてブラウザに表示（自動）
    bodyがないとツールが表示されません（注意）
    """
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>DebugToolbar Test</title>
    </head>
    <body>
        <h1>ハロー、Flask-DebugToolbar！</h1>
        <p>画面の右側を見てね。</p>
    </body>
    </html>
    """


if __name__ == "__main__":
    app.run()
