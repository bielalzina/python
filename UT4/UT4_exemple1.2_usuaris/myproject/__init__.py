import os
from flask import Flask
from flask_login import LoginManager

app = Flask(__name__)

# Cream un objecte de la classe LoginManager
login_manager = LoginManager()

# SECRET_KEY
app.config['SECRET_KEY'] = 'averysecretkey'

# Passam l'objecte creat a la nostra app
login_manager.init_app(app)

# Els usuaris no autenticats seran redirigits a la vista "home"
login_manager.login_view="home"
