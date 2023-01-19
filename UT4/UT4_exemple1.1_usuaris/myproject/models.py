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
        user=User()
        user.fromID(user_id)
        return user

class User(UserMixin):

    id = 0

    def __init__(self):
        self.username="null"

    def fromUsername(self, username):
        self.username=username
        RQ=self.getId()
        if RQ:
            print(RQ)
            self.rol=RQ['rol']
            self.id=RQ['id']
            self.email=RQ['email']

    def fromID(self,Userid):
        # CONNEXIO A BBDD
        db=pymysql.connect(host='localhost',
                            user='root',
                            db='usuarisut4',
                            charset='utf8mb4',
                            autocommit=True,
                            cursorclass=pymysql.cursors.DictCursor)
        cursor=db.cursor()
        sql="SELECT id,usuari,email,rol FROM usuaris WHERE id="+str(Userid)
        cursor.execute(sql)
        ResQuery=cursor.fetchone()
        if ResQuery:
            self.id=ResQuery['id']
            self.rol=ResQuery['rol']
            self.email=ResQuery['email']
            self.username=ResQuery['usuari']
    
    def comprovaUsuari(self,pwd):
        # CONNEXIO A BBDD
        db=pymysql.connect(host='localhost',
                            user='root',
                            db='usuarisut4',
                            charset='utf8mb4',
                            autocommit=True,
                            cursorclass=pymysql.cursors.DictCursor)
        cursor=db.cursor()
        sql="SELECT count(*) FROM usuaris WHERE usuari='"+self.username+"'"
        cursor.execute(sql)
        ResQuery=cursor.fetchone()
        if ResQuery['count(*)']==1:
            sql="SELECT password FROM usuaris WHERE usuari='"+self.username+"'"
            cursor.execute(sql)
            ResQuery=cursor.fetchone()
            resposta=check_password_hash(ResQuery['password'],pwd)
            self.getId()
        else:
            resposta=False
        db.close()
        return resposta

    def getId(self):
        # CONNEXIO A BBDD
        db=pymysql.connect(host='localhost',
                            user='root',
                            db='usuarisut4',
                            charset='utf8mb4',
                            autocommit=True,
                            cursorclass=pymysql.cursors.DictCursor)
        cursor=db.cursor()
        sql="SELECT id,email,rol FROM usuaris WHERE usuari='"+self.username+"'"
        cursor.execute(sql)
        ResQuery=cursor.fetchone()
        if ResQuery:
            self.id=ResQuery['id']
            self.rol=ResQuery['rol']
            self.email=ResQuery['email']
            return ResQuery
        else:
            return False

    def getUsername(self):
        return self.username

    def nouUsuari(self,username,password,email):
        # CONNEXIO A BBDD
        db=pymysql.connect(host='localhost',
                            user='root',
                            db='usuarisut4',
                            charset='utf8mb4',
                            autocommit=True,
                            cursorclass=pymysql.cursors.DictCursor)
        cursor=db.cursor()
        sql="SELECT max(id)+1 nouId FROM usuaris"
        cursor.execute(sql)
        ResQuery=cursor.fetchone()
        sql = "INSERT INTO usuaris VALUES("+str(ResQuery['nouId'])+",'"+username
        sql = sql + "','"+generate_password_hash(password)+"','"+email+"','user')"
        cursor.execute(sql)
        #return ResQuery['nouId']

    def modificaUsuari(self,idusuari,email,password):
        # CONNEXIO A BBDD
        db=pymysql.connect(host='localhost',
                            user='root',
                            db='usuarisut4',
                            charset='utf8mb4',
                            autocommit=True,
                            cursorclass=pymysql.cursors.DictCursor)
        cursor=db.cursor()
        sql="UPDATE usuaris SET password='"+generate_password_hash(password)+"',email='"+email+"' WHERE ID="+str(idusuari)
        cursor.execute(sql)


