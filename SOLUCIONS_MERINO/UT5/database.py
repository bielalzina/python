import pymysql.cursors
from werkzeug.security import generate_password_hash, check_password_hash
import datetime


class gimnas(object):

    def datetimeToStrYMD(self, data):
        data = data.strftime("%Y-%m-%d")
        return data

    def connecta(self):
        # CONNEXIO A BBDD
        self.db = pymysql.connect(host='localhost',
                                  user='root',
                                  db='gimnasUT5repas',
                                  charset='utf8mb4',
                                  autocommit=True,
                                  cursorclass=pymysql.cursors.DictCursor)
        self.cursor = self.db.cursor()

    def desconnecta(self):
        self.db.close()

    def tornaUsuaris(self):
        sql = "SELECT id, username, email, nom, llinatges, telefon, diaalta FROM usuaris;"
        self.cursor.execute(sql)
        ResQuery = self.cursor.fetchall()
        # Convertim data OBJECTE a STRING
        for valor in ResQuery:
            valor['diaalta'] = self.datetimeToStrYMD(valor['diaalta'])
        return ResQuery

    def desaNouUsuari(self, campJson):
        # Comprovam que el nom d'usuari No estigui ocupat
        sql = "SELECT count(*) existeix FROM usuaris "
        sql = sql + "WHERE username='"+campJson['username']+"';"
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        if result['existeix'] == 1:
            return ("USUARI EXISTENT, PROVA AMB UN ALTRE")
        else:
            # Obtenim ID pel nou usuari
            sql = "SELECT MAX(id)+1 nouID from usuaris;"
            self.cursor.execute(sql)
            nouID = self.cursor.fetchone()

            # Generam HASH pel password
            campJson['password'] = generate_password_hash(campJson['password'])

            # Afegim usuari
            sql = "INSERT INTO usuaris (id"
            for index in campJson:
                sql = sql + ","+index
            sql = sql + ") VALUES ("+str(nouID['nouID'])
            for valor in campJson:
                sql = sql + ",'"+campJson[valor]+"'"
            sql = sql + ");"
            self.cursor.execute(sql)

            # Retornam ID nou usuari
            sql = "SELECT MAX(id) nouID from usuaris;"
            self.cursor.execute(sql)
            nouID = self.cursor.fetchone()
            return nouID['nouID']

    def tornaUsuariPerID(self, idusuari):
        sql = "SELECT id, username, email, nom, llinatges, telefon, diaalta FROM usuaris "
        sql = sql + "WHERE id="+str(idusuari)
        self.cursor.execute(sql)
        ResQuery = self.cursor.fetchone()
        if ResQuery != None:
            # Convertim data OBJECTE a STRING
            ResQuery['diaalta'] = self.datetimeToStrYMD(ResQuery['diaalta'])
        return ResQuery

    def esborraUsuari(self, idusuari):
        sql = "DELETE FROM usuaris "
        sql = sql + "WHERE id="+str(idusuari)
        self.cursor.execute(sql)
        ResQuery = self.cursor.fetchone()
        return ResQuery

    def modificaUsuariPerID(self, idusuari, campJSON):
        # Generam HASH pel password
        campJSON['password'] = generate_password_hash(campJSON['password'])

        # ACTUALITZAM VALORS
        for valor in campJSON:
            sql = "UPDATE usuaris SET "+valor+"='"+campJSON[valor]+"' "
            sql = sql+"WHERE id="+str(idusuari)
            self.cursor.execute(sql)

        # Retornam usuari modificat
        Resquery = self.tornaUsuariPerID(idusuari)
        return Resquery

    def tornaReservesSegonsData(self, data):
        # print(type(data))
        # print(data)
        # Passam data STR a datetime
        dataOBJ = datetime.datetime.strptime(data, '%Y-%m-%d')
        # print(type(dataOBJ))
        # print(dataOBJ)
        # Obtenim datetime per dilluns
        dillunsOBJ = dataOBJ-datetime.timedelta(days=dataOBJ.weekday())
        # print(type(dillunsOBJ))
        # print(dillunsOBJ)
        # Obtenim datetime per diumenge
        diumengeOBJ = dillunsOBJ + datetime.timedelta(days=7)
        # print(diumengeOBJ)
        # Passam dilluns i diumenge a STR
        dillunsSTR = dillunsOBJ.strftime("%Y-%m-%d")
        diumengeSTR = diumengeOBJ.strftime("%Y-%m-%d")
        sql = "SELECT reserves.data, usuaris.username, pistes.tipo "
        sql = sql + "FROM reserves "
        sql = sql + "INNER JOIN pistes ON reserves.idpista=pistes.idpista "
        sql = sql + "INNER JOIN usuaris ON reserves.idclient=usuaris.id "
        sql = sql + "WHERE data BETWEEN '"+dillunsSTR+"' AND '"+diumengeSTR+"' "
        sql = sql + "ORDER BY reserves.data ASC;"
        self.cursor.execute(sql)
        ResQuery = self.cursor.fetchall()
        # Convertim data OBJECTE a STRING
        for valor in ResQuery:
            valor['data'] = self.datetimeToStrYMD(valor['data'])
        return ResQuery

    def tornaReservesSetmanaActual(self):
        # Obtenim data actual
        dataOBJ = datetime.date.today()
        # Obtenim datetime per dilluns
        dillunsOBJ = dataOBJ-datetime.timedelta(days=dataOBJ.weekday())
        # Obtenim datetime per dilluns següent
        dillunsProperOBJ = dillunsOBJ + datetime.timedelta(days=7)
        # Passam dates a STR
        dillunsSTR = dillunsOBJ.strftime("%Y-%m-%d")
        dillunsProperSTR = dillunsProperOBJ.strftime("%Y-%m-%d")
        sql = "SELECT reserves.data, usuaris.username, pistes.tipo "
        sql = sql + "FROM reserves "
        sql = sql + "INNER JOIN pistes ON reserves.idpista=pistes.idpista "
        sql = sql + "INNER JOIN usuaris ON reserves.idclient=usuaris.id "
        sql = sql + "WHERE data BETWEEN '"+dillunsSTR+"' AND '"+dillunsProperSTR+"' "
        sql = sql + "ORDER BY reserves.data ASC;"
        self.cursor.execute(sql)
        ResQuery = self.cursor.fetchall()
        # print(ResQuery)
        # Convertim data OBJECTE a STRING
        for valor in ResQuery:
            valor['data'] = self.datetimeToStrYMD(valor['data'])
        return ResQuery

    def tornaReservesUsuari(self, idusuari):
        sql = "SELECT reserves.data, pistes.tipo "
        sql = sql + "FROM reserves "
        sql = sql + "INNER JOIN pistes ON reserves.idpista=pistes.idpista "
        sql = sql + "WHERE idclient='"+str(idusuari)+"' "
        sql = sql + "ORDER BY reserves.data ASC;"
        self.cursor.execute(sql)
        ResQuery = self.cursor.fetchall()
        # print(ResQuery)
        # Convertim data OBJECTE a STRING
        for valor in ResQuery:
            valor['data'] = self.datetimeToStrYMD(valor['data'])
        return ResQuery
