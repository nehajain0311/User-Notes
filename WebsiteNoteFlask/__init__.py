
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager #how we find our user

db=SQLAlchemy() #sqlalchmey object which will carry our connection
DB_NAME="database.db"


def create_app():
    app=Flask(__name__)
    app.config['SECRET_KEY']="MYFLASKAPP"
    # our sqlqlchmey database is saved inside the sqlite3 folder of project
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app) #initialise database with our app



    # import the blueprint
    from .views import views
    from .auth import auth

    # to register blueprints with app
    app.register_blueprint(views,url_prefix='/')  #url_prefix means if we want to prefix regex before url on route
    #eg if we say url_prefix='/views/  then the route address in views.py will append after /views/route-address in views.py
    #if we keep it blank it will only take route from @blueprint.route("address here")
    app.register_blueprint(auth, url_prefix='/')

    from .models import Note,User  #this will let us use the note and user models for our app

    create_databse(app) #this creates database associated with our app

    # where to go if user is not logged in
    login_manager = LoginManager()  # this helps to find our user
    login_manager.login_view = 'auth.login'  # redirecting to auth login if user not logged in
    login_manager.init_app(app)  # this register our app with the loginmanger and user

    @login_manager.user_loader
    def load_user(id): #this tell flask how we load our user
        return User.query.get(int(id))

    return app


def create_databse(app): #this function will check if database exist we dont need to create a new one
    if not path.exists('WebsiteNoteFlask/' +DB_NAME):
        db.create_all(app=app) #we already set in app.config where to create the database if not exist
        print('Database Created')
