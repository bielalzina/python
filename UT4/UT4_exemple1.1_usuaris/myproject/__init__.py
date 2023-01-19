import os
from flask import Flask
from flask_login import LoginManager

# Cream objecte Login Manager
login_manager=LoginManager()

app=Flask(__name__)

# Sovint es desa en un arxiu separat config.py
app.config['SECRET_KEY']='mysecretkey'

# Ara podem passar la nostra aplicació al gestor d'inici de sessió
login_manager.init_app(app)

# Els usuaris no logats es redirigeixen a home
login_manager.login_view="home"