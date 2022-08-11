from flask import Flask
from flask_restx import Api
from os import environ
from src.config import DevConfig, PrdConfig
from src.database import db, migrate
from src.controller.user import User
from src.controller.comment import Comment
from api.src.nickname_gen import nick_gen
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)


def create_app():

    api = Api(app)  # Flask 객체에 Api 객체 등록

    if environ.get("FLASK_ENV") == "prd":
        app.config.from_object(PrdConfig())
    else:
        app.config.from_object(DevConfig())

    @app.route('/')
    def hello():
        msg = ""
        for key, val in app.config["DB"].items():
            msg += f"{key}={val}<br>"
        msg += f"{app.config['DB_URI']}<br>"
        msg += f"{app.config['SQLALCHEMY_DATABASE_URI']}<br>"
        return msg

    api.add_namespace(User, '/api/user')
    api.add_namespace(Comment, '/api')

    db.init_app(app)

    migrate.init_app(app, db)
    # with app.app_context():
    #     db.create_all()
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=app.config["DEBUG"], host="0.0.0.0", port=5000)
