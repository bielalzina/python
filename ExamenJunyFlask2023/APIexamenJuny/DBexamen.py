import pymysql.cursors
import sqlalchemy as db
import configparser
from werkzeug.security import generate_password_hash, check_password_hash
import datetime


class vols(object):
    def conecta(self):
        # Conexion a la BBDD del servidor mySQL
        self.db = pymysql.connect(host='localhost',
                                  user='root',
                                  db='vols',
                                  charset='utf8mb4',
                                  autocommit=True,
                                  cursorclass=pymysql.cursors.DictCursor)
        self.cursor = self.db.cursor()

    def desconecta(self):
        self.db.close()

    def cargaAeroports(self):
        sql = "SELECT * from airports"
        self.cursor.execute(sql)
        ResQuery = self.cursor.fetchall()
        return ResQuery

    def cargaArribades(self, aeroport, fecha_hora):
        fechasql = fecha_hora.replace("_", " ")+":00"
        sql = "SELECT * from flights where arrival_airport='"+aeroport
        sql = sql+"' AND arrival_time>='"+fechasql+"' order by arrival_time limit 10"
        self.cursor.execute(sql)
        ResQuery = self.cursor.fetchall()
        return ResQuery

    def cargaSortides(self, aeroport, fecha_hora):
        return "pendent de desenvolupar"

    def tornaPaisAeroport(self, aeroport):
        sql = "SELECT country FROM airports WHERE id_airport='"+aeroport+"';"
        self.cursor.execute(sql)
        ResQuery = self.cursor.fetchone()

        return ResQuery

    def cargaSortidesNacionals(self, aeroport):
        resposta = vols.tornaPaisAeroport(self, aeroport)
        pais = resposta['country']
        sql = "SELECT * FROM flights "
        sql = sql + "JOIN airports ON flights.arrival_airport = airports.id_airport "
        sql = sql + "WHERE flights.departure_airport = '" + \
            aeroport+"' AND airports.country = '"+pais+"'"
        self.cursor.execute(sql)
        ResQuery = self.cursor.fetchall()
        # print(ResQuery)
        return ResQuery

    def cargaSortidesInternacionals(self, aeroport):
        resposta = vols.tornaPaisAeroport(self, aeroport)
        pais = resposta['country']
        sql = "SELECT * FROM flights "
        sql = sql + "JOIN airports ON flights.arrival_airport = airports.id_airport "
        sql = sql + "WHERE flights.departure_airport = '" + \
            aeroport+"' AND airports.country <> '"+pais+"'"
        self.cursor.execute(sql)
        ResQuery = self.cursor.fetchall()
        # print(ResQuery)
        return ResQuery

    def cancelaVol(self, id_vol):
        sql = (
            "UPDATE flights SET cancelado=1 WHERE id_flight='"
            + id_vol
            + "';"
        )
        self.cursor.execute(sql)
        return "FET"
