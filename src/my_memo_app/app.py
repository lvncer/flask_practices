from flask import Flask
from flask_migrate import Migrate
from models import db, User
from flask_login import LoginManager
from auth.views import auth_bp
from memo.views import memo_bp
from wiki.views import wiki_bp


app = Flask(__name__)
# 設定ファイル読み込み
app.config.from_object("config.Config")
# dbとFlaskとの紐づけ
db.init_app(app)
# マイグレーションとの紐づけ（Flaskとdb）
migrate = Migrate(app, db)
# LoginManagerインスタンス
login_manager = LoginManager()
# LoginManagerとFlaskとの紐づけ
login_manager.init_app(app)
# ログインが必要なページにアクセスしようとしたときに表示されるメッセージを変更
login_manager.login_message = "認証していません：ログインしてください"
# 未認証のユーザーがアクセスしようとした際にリダイレクトされる関数名を設定する(ブループリント対応)
login_manager.login_view = 'auth.login'
# blueprintをアプリケーションに登録
app.register_blueprint(auth_bp)
app.register_blueprint(memo_bp)
app.register_blueprint(wiki_bp)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


from views import *


if __name__ == "__main__":
    app.run()
