from myproject import login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import pymysql.cursors

# En heretar l'UserMixin, tenim accés a molts atributs integrats
# que podrem cridar en les nostres vistes!
# is_authenticated()
# is_active()
# is_anonymous()
# get_id()

# El decorador user_loader permet a flask-login carregar l'usuari actual
# i agafa el seu identificador.
@login_manager.user_loader
def load_user(user_id):
    if user_id:
        # Instanciam la classe User(Mixin)
        userLM=User()
        userLM.obtenirDadesUserLM(user_id)
        print()
        print("LOGIN_MANAGER:")
        print(userLM)
        print(userLM.id)
        print(userLM.nomUsuari)
        print(userLM.password)
        print(userLM.email)
        print(userLM.rol)
        return userLM


class User(UserMixin):
    
    id = 0
    
    # CONSTRUCTOR
    def __init__(self):
        self.nomUsuari = "null"
        
    def set_nomUsuari(self, usuari):
        self.nomUsuari = usuari

    def obtenirDadesUserLM(self,userid):
        # CONNEXIO A BBDD
        db=pymysql.connect(host='localhost',
                            user='root',
                            db='usuarisut4',
                            charset='utf8mb4',
                            autocommit=True,
                            cursorclass=pymysql.cursors.DictCursor)
        cursor=db.cursor()
        sql = "SELECT * FROM usuaris WHERE id="+str(userid)
        cursor.execute(sql)
        resultatConsulta=cursor.fetchone()
        if resultatConsulta:
            self.id=resultatConsulta['id']
            self.usuari=resultatConsulta['usuari']
            self.password=resultatConsulta['password']
            self.email=resultatConsulta['email']
            self.rol=resultatConsulta['rol']
        db.close()
        
    def comprovaPassword(self, contrasenya):
        # CONNEXIO A BBDD
        db=pymysql.connect(host='localhost',
                            user='root',
                            db='usuarisut4',
                            charset='utf8mb4',
                            autocommit=True,
                            cursorclass=pymysql.cursors.DictCursor)
        cursor=db.cursor()
        sql = "SELECT count(*) FROM usuaris WHERE usuari='"+self.nomUsuari+"'"
        cursor.execute(sql)
        resultatConsulta1=cursor.fetchone()
        if resultatConsulta1['count(*)']==1:
            # Existeix un únic registre amb aquest usuari
            sql = "SELECT password FROM usuaris WHERE usuari='"+self.nomUsuari+"'"
            cursor.execute(sql)
            resultatConsulta2=cursor.fetchone()
            # Resposta pot ser TRUE (password->OK) o FALSE (password->KO)
            resposta = check_password_hash(resultatConsulta2['password'],contrasenya)
        # NO existeix cap registre amb aquest usuari o més d'un registre
        else:
             resposta=False
        db.close()
        return resposta

    
    def obtenirDadesUsuariSegonsNomUsuari(self):
        # CONNEXIO A BBDD
        db=pymysql.connect(host='localhost',
                            user='root',
                            db='usuarisut4',
                            charset='utf8mb4',
                            autocommit=True,
                            cursorclass=pymysql.cursors.DictCursor)
        cursor=db.cursor()
        sql = "SELECT * FROM usuaris WHERE usuari='"+self.nomUsuari+"'"
        cursor.execute(sql)
        resultatConsulta=cursor.fetchone()
        if resultatConsulta:
            self.id=resultatConsulta['id']
            self.nomUsuari=resultatConsulta['usuari']
            self.password=resultatConsulta['password']
            self.email=resultatConsulta['email']
            self.rol=resultatConsulta['rol']
        db.close() 
        
        
