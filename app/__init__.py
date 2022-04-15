from flask import Flask
from flask_login import LoginManager

app = Flask(__name__)

login = LoginManager(app)
login.init_app(app)
login.login_view = 'login'
app.secret_key = 'dev'

from app import routes, models

app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
app.config['UPLOAD_PATH'] = 'uploads'
