from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, SubmitField, DateField)
from wtforms.validators import (DataRequired, Regexp, Length, Email, 
                                ValidationError, EqualTo)
import datetime
import html


# VALIDAM QUE USERNAME NO CONTENGUI PARAULES OFENSIVES
def validaUserName(form, camp):
    paraulesOfensives=['caca','pedo','culo','pis','java','php','carapolla',
                       'potorro','gilipollas']
    for paraula in paraulesOfensives:
        if paraula in camp.data:
            raise ValidationError(f"La paraula \"{paraula}\" no està permesa") 


# VALIDAM QUE DATA ALTA <= AVUI
def validaDataAlta(form, camp):
  avui=datetime.date.today()
  if camp.data > avui:
    raise ValidationError(f"La data d\'alta no pot ser posterior a avui")

# Cream una classe WTFORMS

class InfoForm(FlaskForm):
    username = StringField('NOM D\'USUARI:', 
                       validators=[DataRequired(),
                                   Length(min=6, max=15,
                                          message='El nom d\'usuari ha de tenir \
                                            una longitud mìnima de %(min)d \
                                            caràcters i màxima de %(max)d \
                                            caràcters'),
                                   validaUserName])

   
    nom = StringField('EL TEU NOM:', 
                       validators=[DataRequired(),
                                   Length(max=50,
                                          message='El teu nom pot tenir una \
                                            una longitud màxima de %(max)d \
                                            caràcters')])

    llinatges = StringField('ELS TEUS LLINATGES:', 
                       validators=[DataRequired(),
                                   Length(max=50,
                                          message='Els teus llinatges poden \
                                            tenir una longitud màxima de \
                                            %(max)d caràcters')])
    
    password= PasswordField('PASSWORD:',
      validators=[DataRequired(),
      Regexp('^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$',
      message='El password he de tenir una longitud mínima de 8 caràcters. \
        Com a mínim ha d\'incloure una majúscula, una minúscula, un número \
        i un caràcter especial: #?!@$%^&*-')])
    
    confirm_password= PasswordField('TORNA A INTRODUIR EL PASSWORD:',
                             validators=[DataRequired(),
                                        EqualTo('password', message='Els passwords \
                                          no coincideixen')])
    
    dataAlta = DateField('DIA D\'ALTA:',
                             validators=[DataRequired(),
                                         validaDataAlta])
    
    email = StringField('@ E-MAIL:',
                       validators=[DataRequired(),
                       Email(message='El mail indicat té un format incorrecte')])

    telefon = StringField('EL TEU TELÈFON:', 
      validators=[DataRequired(),
      Regexp('^(\+|00)\(?\d{1,3}\)?\s?\d{1,5}\s?\d{5,7}$',
      message='Exemples vàlids de format telèfonic: \
                  +(12) 123 123456  ó  00(12) 123 123456  ó  +12 123 123456  ó  \
                  0012 123 123456  ó  0012123123456')])

    
    btnEnviar = SubmitField('ENVIAR')