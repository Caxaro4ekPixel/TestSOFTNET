from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_praetorian import Praetorian
from importlib import import_module
from flask_login import LoginManager

db = SQLAlchemy()
guard = Praetorian()
login_manager = LoginManager()


def create_app(app_config):
    app = Flask(__name__)

    app.config.from_object(app_config)

    db.init_app(app)

    from .models import User, Dashboard, Note

    guard.init_app(app, user_class=User)

    from .api import api as api_blueprint
    import_module('app.api.route')
    app.register_blueprint(api_blueprint)

    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.app_context():
        db.create_all()

    @app.before_first_request
    def create_default_user():
        if not User.query.filter_by(username=app_config.default_user_credo['username']).first():
            db.session.add(User(username=app_config.default_user_credo['username'], password=app_config.default_user_credo['password'], roles='admin'))
            db.session.commit()

    return app
