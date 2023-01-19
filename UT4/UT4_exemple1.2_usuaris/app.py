from myproject import app
from flask import render_template, redirect, request, url_for
from flask_login import login_user, login_required, logout_user, current_user
from myproject.models import User
from werkzeug.security import generate_password_hash, check_password_hash

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods = ['GET','POST'])
def login():
    # Obtenim dades del formulari
    usuari=request.form['usuari']
    password=request.form['password']
    print(usuari)
    print(password)
    
    # Instaciam la CLASSE User
    user=User()
    print(user)
    print(user.nomUsuari)
    
    # Definim l'atribut nomUsuari de l'objecte user
    user.set_nomUsuari(usuari)
    print(user.nomUsuari)
    
    if user.comprovaPassword(password):
        # TRUE, password -> OK
        # Definim els atributs id, email, rol de l'objecte user
        user.obtenirDadesUsuariSegonsNomUsuari()
        print()
        print(user.id)
        print(user.nomUsuari)
        print(user.password)
        print(user.email)
        print(user.rol)
        
        
        # Carregam usuari en login_manager
        login_user(user)
        
        
        return redirect(url_for('welcome_user'))
        
        
    
    else:
        # FALSE, password -> KO
        return render_template('login.html', 
                               loginMissatge="Usuari i/o password incorrectes")


@app.route('/benvinguda')
@login_required
def welcome_user():
    return render_template('padentro.html')


if __name__ == '__main__':
    app.run(debug=True)