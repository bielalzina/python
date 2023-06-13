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

    def novaReservaUsuari(self, idusuari, campJSON):
        print(idusuari)
        print(type(idusuari))
        print(campJSON['data'])
        print(type(campJSON['data']))
        print(campJSON['idpista'])
        print(type(campJSON['idpista']))

        # comprovam data i hora correcta
        retorn = 0
        # separam data i hora
        dataHora = campJSON['data'].split(sep=" ")
        print(dataHora[0])
        print(dataHora[1])

        # Comprovem DATA
        dataOBJ = datetime.datetime.strptime(dataHora[0], '%Y-%m-%d')
        # print(dataOBJ.weekday())
        if (dataOBJ.weekday() > 4):
            return ("DATA INCORRECTA")
        # Comprovem DATA
        hora = dataHora[1].split(":")
        print(hora[0])
        print(type(hora[0]))
        if (int(hora[0]) < 15 or int(hora[0]) > 20):
            return ("HORA INCORRECTA")

        # Comprovam disponibilitat
        data = dataHora[0]+" "+hora[0]+":00:00"
        print(data)
        print(type(data))
        dataHoraOBJ = datetime.datetime.strptime(data, '%Y-%m-%d %H:%M:%S')
        print(dataHoraOBJ)
        print(type(dataHoraOBJ))

        llistaReserves = self.tornaReserves()
        # print(llistaReserves)

        for reserva in llistaReserves:
            if (reserva['data'] == dataHoraOBJ and reserva['idpista'] == campJSON['idpista']):
                return ("PISTA OCUAPADA, PROVA UNA ALTRA OPCIÓ")

        # INSERIM RESERVA
        sql = "INSERT INTO reserves (data,idpista,idclient) "
        sql = sql + "VALUES ('"+data+"', " + \
            str(campJSON['idpista'])+", "+str(idusuari)+");"
        self.cursor.execute(sql)
        # retornam llista de reserves d'aquest usuari

        llistaReservesUusari = self.tornaReservesUsuari(idusuari)
        return llistaReservesUusari

    def tornaReserves(self):

        sql = "SELECT * FROM reserves "
        self.cursor.execute(sql)
        ResQuery = self.cursor.fetchall()

        return ResQuery
