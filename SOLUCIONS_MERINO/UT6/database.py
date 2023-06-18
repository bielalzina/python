import pymysql.cursors


class whatspau(object):

    def conecta(self):
        # CONNEXIÓ A BBDD
        self.db = pymysql.connect(host='localhost',
                                  user='root',
                                  db='whatspauUT6repas',
                                  charset='utf8mb4',
                                  autocommit=True,
                                  cursorclass=pymysql.cursors.DictCursor)
        self.cursor = self.db.cursor()

    def desconecta(self):
        self.db.close()

    def tornaUsernames(self, idUserAut):
        sql = "SELECT username FROM users_base WHERE id_user<>"+str(idUserAut)
        self.cursor.execute(sql)
        ResQuery = self.cursor.fetchall()
        return ResQuery

    def tornaTotsMissatgesSend(self):
        sql = "SELECT m.fecha, s.username as sender_username, "
        sql = sql + "r.username as receiver_username, m.missatge, m.status "
        sql = sql + "FROM missatges m "
        sql = sql + "JOIN users_base s ON m.id_sender=s.id_user "
        sql = sql + "JOIN users_base r ON m.id_receiver=r.id_user "
        sql = sql + "WHERE m.status='send' "
        sql = sql + "ORDER BY m.fecha;"
        self.cursor.execute(sql)
        ResQuery = self.cursor.fetchall()
        # Convertim fecha a string
        for valor in ResQuery:
            valor['fecha'] = valor['fecha'].strftime("%Y-%m-%d %H:%M:%S")
        return ResQuery

    def tornaNumMissatges(self, idUserAut):
        sql = "SELECT COUNT(status) FROM missatges "
        sql = sql + "WHERE status='send' "
        sql = sql + "AND (id_sender="+str(idUserAut) + \
            " OR id_receiver="+str(idUserAut)+")"
        self.cursor.execute(sql)
        ResQuery = self.cursor.fetchone()
        return ResQuery['COUNT(status)']

    def tornaConversa(self, id_interlocutor, idUserAut):
        sql = "SELECT m.fecha, s.username as sender_username, "
        sql = sql + "r.username as receiver_username, m.missatge, m.status "
        sql = sql + "FROM missatges m "
        sql = sql + "JOIN users_base s ON m.id_sender=s.id_user "
        sql = sql + "JOIN users_base r ON m.id_receiver=r.id_user "
        sql = sql + "WHERE ((m.id_sender="+str(id_interlocutor)+" "
        sql = sql + "AND m.id_receiver="+str(idUserAut)+") "
        sql = sql + "OR (m.id_sender="+str(idUserAut)+" "
        sql = sql + "AND m.id_receiver="+str(id_interlocutor)+")) "
        sql = sql + "ORDER BY m.fecha;"
        self.cursor.execute(sql)
        ResQuery = self.cursor.fetchall()
        # Convertim fecha a string
        for valor in ResQuery:
            valor['fecha'] = valor['fecha'].strftime("%Y-%m-%d %H:%M:%S")
        return ResQuery

    def nouMissatge(self, id_interlocutor, idUserAut, campJSON):
        sql = "INSERT INTO missatges (fecha, id_sender, id_receiver, "
        sql = sql + "missatge, status) "
        sql = sql + "VALUES (now(), '"+str(idUserAut) + \
            "', '"+str(id_interlocutor)+"', "
        sql = sql + "'"+str(campJSON['text'])+"', 'send');"
        self.cursor.execute(sql)
        # Tornam conversa amb usuari
        Resquery = self.tornaConversa(id_interlocutor, idUserAut)
        return Resquery

    def canviaStatusRebut(self, idUserAut):
        sql = "UPDATE missatges SET status='received' "
        sql = sql + "WHERE status='send' AND id_receiver="+str(idUserAut)
        print(sql)
        # EXECUTAM TRY - EXCEPT
        try:
            self.cursor.execute(sql)
            return ('STATUS MODIFICAT A REBUT')
        except:
            return ('NO S\'HA POGUT MODIFICAR STATUS')

    def canviaStatusLlegit(self, idUserAut):
        sql = "UPDATE missatges SET status='read' "
        sql = sql + "WHERE status='received' AND id_receiver="+str(idUserAut)
        print(sql)
        # EXECUTAM TRY - EXCEPT
        try:
            self.cursor.execute(sql)
            return ('STATUS MODIFICAT A REBUT')
        except:
            return ('NO S\'HA POGUT MODIFICAR STATUS')
