from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from config import Config
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
login = LoginManager(app)
mail = Mail(app)
cors = CORS(app, origins=['http://localhost:8000', 'https://psleziona.github.io'], supports_credentials=True)



from app import routes