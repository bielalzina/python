import pymysql.cursors
import sqlalchemy as db
import configparser
from werkzeug.security import generate_password_hash,check_password_hash
import datetime


class vols(object):
    def conecta(self):
        #Conexion a la BBDD del servidor mySQL
        self.db = pymysql.connect(host='localhost',
                                     user='root',
                                     db='vols',
                                     charset='utf8mb4',
                                     autocommit=True,
                                     cursorclass=pymysql.cursors.DictCursor)
        self.cursor=self.db.cursor()

    def desconecta(self):
        self.db.close()

    def cargaAeroports(self):
        sql="SELECT * from airports"
        self.cursor.execute(sql)
        ResQuery=self.cursor.fetchall()
        return ResQuery

    def cargaArribades(self,aeroport,fecha_hora):
        fechasql=fecha_hora.replace("_"," ")+":00"
        sql="SELECT * from flights where arrival_airport='"+aeroport
        sql=sql+"' AND arrival_time>='"+fechasql+"' order by arrival_time limit 10";
        self.cursor.execute(sql)
        ResQuery=self.cursor.fetchall()
        return ResQuery             

    def cargaSortides(self,aeroport,fecha_hora):
        return "pendent de desenvolupar"

 