import pymysql.cursors
import random
import joblib
import json
import sqlalchemy as db
from dateutil.parser import parse
import datetime


class gimnas (object):

    # DATETIME TO STR ("%d-%m-%Y")

    def datetimeToStrDMY(data):
        dataStr = data.strftime("%d-%m-%Y")
        return dataStr

    # DATETIME TO STR ("%Y-%m-%d")

    def datetimeToStrYMD(data):
        dataStr = data.strftime("%Y-%m-%d")
        return dataStr

    # DATA STR A OBJECTE DATETIME ("%d-%m-%Y")

    def strToDatetime(data):
        dataObj = datetime.datetime.strptime(data, '%d-%m-%Y')
        return dataObj

    def carregaUsuaris():
        # CONNEXIO A BBDD
        db = pymysql.connect(host='localhost',
                             user='root',
                             db='gimnas2',
                             charset='utf8mb4',
                             autocommit=True,
                             cursorclass=pymysql.cursors.DictCursor)
        cursor = db.cursor()
        sql = "SELECT * from clients"
        cursor.execute(sql)
        ResQuery = cursor.fetchall()
        db.close()
        # print(ResQuery)
        return ResQuery

    def carregaReserves(dia):
        # CONNEXIO A BBDD
        db = pymysql.connect(host='localhost',
                             user='root',
                             db='gimnas2',
                             charset='utf8mb4',
                             autocommit=True,
                             cursorclass=pymysql.cursors.DictCursor)
        cursor = db.cursor()
        inici = gimnas.strToDatetime(dia)
        final = inici + datetime.timedelta(days=5)
        iniciStr = gimnas.datetimeToStrYMD(inici)
        finalStr = gimnas.datetimeToStrYMD(final)
        sql = "SELECT r.data, p.tipo, c.nom, c.llinatges "
        sql = sql + "FROM reserves r,  pistes p, clients c "
        sql = sql + "WHERE r.idpista=p.idpista AND r.idclient=c.idclient "
        sql = sql + "AND r.data>='"+iniciStr+"' "
        sql = sql + "AND r.data<='"+finalStr+"';"
        print(sql)
        cursor.execute(sql)
        ResQuery = cursor.fetchall()
        print(ResQuery)
        db.close()
        return ResQuery

    def comprovaDisponibilitat(dia, hora, pista):
        # CONNEXIO A BBDD
        db = pymysql.connect(host='localhost',
                             user='root',
                             db='gimnas2',
                             charset='utf8mb4',
                             autocommit=True,
                             cursorclass=pymysql.cursors.DictCursor)
        cursor = db.cursor()
        dataHora = dia+" "+str(hora)+":00:00"
        sql = "SELECT count(*) p FROM reserves "
        sql = sql + "WHERE  data='"+dataHora+"' AND idpista="+pista+";"
        cursor.execute(sql)
        ResQuery = cursor.fetchone()
        ocupada = ResQuery['p']
        print(ocupada)
        db.close()
        return ocupada

    def reservaPista(diahora, pista, client):
        # CONNEXIO A BBDD
        db = pymysql.connect(host='localhost',
                             user='root',
                             db='gimnas2',
                             charset='utf8mb4',
                             autocommit=True,
                             cursorclass=pymysql.cursors.DictCursor)
        cursor = db.cursor()

        sql = "INSERT INTO reserves "
        sql = sql + "VALUES ('"+diahora+"',"+pista+","+client+");"
        print(sql)
        cursor.execute(sql)
        ResQuery = cursor.fetchall()
        db.close()
