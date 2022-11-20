from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager


bd= SQLAlchemy()
DB_NAME="base.db"
Upload_folder='website/static/upload/'
app = Flask(__name__)
app.config['SECRET_KEY']='pratham'
app.config['SQLALCHEMY_DATABASE_URI']=f"sqlite:///{DB_NAME}"
app.config['Upload_folder']=Upload_folder
bd.init_app(app)

def create_app():


    
    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from .data import User,Institute,Institutedata,Userdata
    create_database(app)
    login_mamager=LoginManager()
    login_mamager.login_view='views.login'
    login_mamager.init_app(app)
    @login_mamager.user_loader
    def load_user(id):
        try:
            user=User.query.get(int(id))
            if user.type=='user':
                return user
            else:
                institute=Institute.query.get(int(id))
                return institute
        except:
                institute=Institute.query.get(int(id))
                return institute

    return app
def create_database(app):
    if not path.exists('website/'+DB_NAME):
        bd.create_all(app=app)
        print("database created")
