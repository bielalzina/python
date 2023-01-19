import os
from flask import Flask
from flask_login import LoginManager

# Cream objecte login_manager de la CLASS LoginManager
login_manager=LoginManager()

# Instanciam la nostra aplicació
app = Flask(__name__)

# SecretKey
app.config['SECRET_KEY']='averysecretkey'

# Passam l'objecte login_manager a l'aplicació
login_manager.init_app(app)

# Els usuaris no logats només poden accedir al template per fer LOGIN
login_manager.login_view="formlogin"

