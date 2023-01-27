from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, SubmitField, DateField,
                     SelectField)
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


# VALIDAM QUE DATA RESERVA >= AVUI
def validaDataAlta(form, camp):
  avui=datetime.date.today()
  if camp.data > avui:
    raise ValidationError(f"La data d\'alta no pot ser posterior a avui")
  
# VALIDAM QUE NO ES PUGUI FER RESERVA EN CAPS DE SETMANA
#def comprovaCapsSetmana(form, camp):


# Cream una classe WTFORMS

class UsuariForm(FlaskForm):
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
                         default=datetime.date.today(),
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

# VALIDAM QUE DIA RESERVA >= AVUI
def validaDiaReserva(form, camp):
  avui=datetime.date.today()
  if camp.data < avui:
    raise ValidationError(f"Només es pot sol·licitar una reserva per avui o \
      dia posterior")


# VALIDAM QUE DIA RESERVA NO SIGUI DISSABTE NI DIUMENGE
def validaCapSetmana(form, camp):
  diaSetmana=camp.data.strftime("%w")
  if diaSetmana=="0" or diaSetmana=="6":
    raise ValidationError(f"No es possible sol·licitar una reserva per DISSABTE \
      o DIUMENGE")



class ReservaForm(FlaskForm):
  dataReserva = DateField('DATA:',
                         default=datetime.date.today(),
                             validators=[DataRequired(),
                                         validaDiaReserva,
                                         validaCapSetmana])
  
  horaReserva = SelectField('HORA',
                            choices=[(15, '15:00 - 16:00'), 
                                     (16, '16:00 - 17:00'),
                                     (17, '17:00 - 18:00'),
                                     (18, '18:00 - 19:00'),
                                     (19, '19:00 - 20:00'),
                                     (20, '20:00 - 21:00')],
                            validators=[DataRequired()])
  
  tipusPista = SelectField('SELECCIONA LA PISTA',
                           validators=[DataRequired()])


  btnEnviar = SubmitField('ENVIAR')