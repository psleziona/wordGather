from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
login = LoginManager(app)
cors = CORS(app, resources='http://localhost:8000/', support_credentials=True)


from app import routes