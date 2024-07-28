from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME ='database.db'


def create_app():
    app = Flask(__name__)
    #secret key for app
    app.config['SECRET_KEY'] = 'hello'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    
    from .views import views
    from .auth import auth
    
    app.register_blueprint(views, url_prefix = '/')
    app.register_blueprint(auth, url_prefix = '/')

    from . models import User, Note
 
    create_database(app)

    # To tell flask where to go when were not logged in
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    #telling flask what user were looking for 
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

#checks if database exists, if not it creates it

def create_database(app):
    print('outside')
    if not path.exists('website/' + DB_NAME):
        print('inside')
        with app.app_context():
            db.create_all()
        print('Created Database!')
