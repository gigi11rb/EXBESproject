from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY']="jakbdkcjajkbshh1o2u197319256657AKJDA#2"
app.config["SQLALCHEMY_DATABASE_URI"]= "sqlite:///data.db" 


app.config["SQLALCHEMY_BINDS"] = {
    "skiing": "sqlite:///skiing.db",
    "snowboarding": "sqlite:///snowboarding.db"
}

login_manager = LoginManager(app)

db = SQLAlchemy(app)
