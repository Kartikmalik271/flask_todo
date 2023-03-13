from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

# defining database
db = SQLAlchemy()
DATABASE_NAME = "database.db"


#setting up the flask app
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY']='dwewr875fyiwocs234wcDSFSW41xxcv' #secure the cookies & session data
    app.config['SQLALCHEMY_DATABASE_URI']=f'sqlite:///{DATABASE_NAME}'
    db.init_app(app)


    from .views import views
    from .auth import auth

#adding routes to the blueprint
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

# creating database
    from .models import User,Todo
    create_database(app)

# protecting user session and routes
    login_manager=LoginManager()
    login_manager.login_view='auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

# to check if database exists , if not then create it
def create_database(app):
    with app.app_context():
        db.create_all()
        print('DataBase Created')