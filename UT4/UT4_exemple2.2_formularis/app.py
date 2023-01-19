from flask import Flask, render_template, flash, session, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import (StringField, BooleanField, DateTimeField, 
                     RadioField, SelectField, TextAreaField, SubmitField)
from wtforms.validators import DataRequired, ValidationError


app=Flask(__name__)


# Configuram SECRET_KEY
app.config['SECRET_KEY']='mysecretkey'


# VALIDACIÓ NOM D'USUARI
def validaUsername(form, nomUsuari):
    if len(nomUsuari.data) < 5:
        raise ValidationError('EL NOM D\'USUARI HA DE TENIR MÉS DE 5 CARACTERS')
    caractersExclosos = "*?!'^+%&/()=}][{$#"
    for char in nomUsuari.data:
        if char in caractersExclosos:
            raise ValidationError(f"EL CARÀCTER {char} NO ESTÀ PERMÉS")


# Cream una classe WTFORMS
# Lots of fields available:
# http://wtforms.readthedocs.io/en/stable/fields.html

class InfoForm(FlaskForm):
    nomUsuari = StringField('INDICA EL TEU NOM D\'USUARI', 
                       validators=[DataRequired(),
                                   validaUsername])
    btnEnviar = SubmitField('ENVIAR')

@app.route('/', methods=['GET','POST'])
def index():
    
    # Cream una instancia de la classe InfoForm anteriorment
    form = InfoForm()
    
    # Si s'ha enviat i validat el formulari, rebem els valors per POST
    if form.validate_on_submit():
        
        # Desam els valors en variables de sessió
        session['nomUsuari']=form.nomUsuari.data 
                
        # Redirigim a resultats.html
        return redirect(url_for('resultat'))
    
    # Si NO s'ha enviat el formulari,
    # o s'ha enviat però NO ha estat validat,
    # cal tornar carregar el formulari passant les dades necessaries
    # per construir-lo (instacia form)
    return render_template('index.html', form=form) 

@app.route('/resultat')
def resultat():
    return render_template('resultat.html') 

if __name__ == '__main__':
    app.run(debug=True)