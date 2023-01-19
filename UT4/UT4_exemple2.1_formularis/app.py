from flask import Flask, render_template, flash, session, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import (StringField, BooleanField, DateTimeField, 
                     RadioField, SelectField, TextAreaField, SubmitField)
from wtforms.validators import DataRequired, Regexp

app=Flask(__name__)

# Configuram SECRET_KEY
app.config['SECRET_KEY']='mysecretkey'

# Cream una classe WTFORMS
# Lots of fields available:
# http://wtforms.readthedocs.io/en/stable/fields.html

class InfoForm(FlaskForm):
    raza = StringField('QUINA ÉS LA TEVA RAÇA', 
                       validators=[DataRequired()])
    castrat = BooleanField('HAS ESTAT CASTRAT')
    estatAnim = RadioField('SELECCIONA EL TEU ESTAT D\'ÀNIM',
                           choices=[('estat_feliç','FELIÇ'),
                                    ('estat_excitat','EXCITAT')])
    menjarFavorit = SelectField('SELECCIONA EL TEU MENJAR FAVORIT',
                                choices=[('poll','POLLASTRE'),
                                    ('vad','VADELLA'),
                                    ('px','PEIX'),])
    telefon = StringField('INTRODUEIX EL TEU TELEFON [9 digìts]',
                          validators = [DataRequired(),
                                        Regexp('^[0-9]{9}$',
                                        message= 'EL TELEFON HA DE TENIR 9 DIGÌTS')])
    comentari = TextAreaField()
    btnEnviar = SubmitField('ENVIAR')

@app.route('/', methods=['GET','POST'])
def index():
    
    # Cream una instancia de la classe InfoForm anteriorment
    form = InfoForm()
    
    # Si s'ha enviat i validat el formulari, rebem els valors per POST
    if form.validate_on_submit():
        
        # Desam els valors en variables de sessió
        session['raza']=form.raza.data 
        session['castrat']=form.castrat.data 
        session['estatAnim']=form.estatAnim.data 
        session['menjarFavorit']=form.menjarFavorit.data 
        session['telefon']=form.telefon.data 
        session['comentari']=form.comentari.data 
        session['btnEnviar']=form.btnEnviar.data 
        
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