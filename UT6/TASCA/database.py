import pymysql.cursors

class whatspau(object):

    def conecta(self):
        # CONNEXIÓ A BBDD
        self.db = pymysql.connect(host='localhost',
                                  user='root',
                                  db='whatspau',
                                  charset='utf8mb4',
                                  autocommit=True,
                                  cursorclass=pymysql.cursors.DictCursor)
        self.cursor=self.db.cursor()

    def desconecta(self):
        self.db.close()

    def dataToString(self,data):
        dataString = data.strftime("%d/%m/%Y - %H:%M:%S")
        return dataString
        



    def tornaUsername(self,idUserAut):
        sql = "SELECT username FROM users_base WHERE id_user<>"+str(idUserAut)
        self.cursor.execute(sql)
        ResQuery=self.cursor.fetchall()
        return ResQuery

    def tornaTotsMissatges(self):
        sql = "SELECT m.fecha, s.username as sender_username,"
        sql = sql + " r.username as receiver_username, m.missatge, m.status"
        sql = sql + " FROM missatges m"
        sql = sql + " JOIN users_base s ON m.id_sender = s.id_user"
        sql = sql + " JOIN users_base r ON m.id_receiver = r.id_user"
        sql = sql + " WHERE m.status='send'"
        sql = sql + " ORDER BY m.fecha"
        self.cursor.execute(sql)
        ResQuery=self.cursor.fetchall()
        # Convertim data a string
        for valor in ResQuery:
            valor['fecha']=self.dataToString(valor['fecha'])
        return ResQuery
    
    def tornaNumMissatges(self,idUserAut):
        sql = "SELECT COUNT(status) FROM missatges "
        sql = sql + " WHERE status='send'"
        sql = sql + " AND (id_sender="+str(idUserAut)
        sql = sql + " OR id_receiver="+str(idUserAut)
        sql = sql + ")"
        self.cursor.execute(sql)
        ResQuery=self.cursor.fetchone()
        return ResQuery['COUNT(status)']

    def tornaMissatgesConversa(self, idInterlocutor, idUserAut):
        sql = "SELECT m.fecha, s.username as sender_username,"
        sql = sql + " r.username as receiver_username, m.missatge, m.status"
        sql = sql + " FROM missatges m"
        sql = sql + " JOIN users_base s ON m.id_sender = s.id_user"
        sql = sql + " JOIN users_base r ON m.id_receiver = r.id_user"
        sql = sql + " WHERE (m.id_sender="+str(idUserAut)
        sql = sql + " AND m.id_receiver="+str(idInterlocutor)
        sql = sql + ")"
        sql = sql + " OR (m.id_sender="+str(idInterlocutor)
        sql = sql + " AND m.id_receiver="+str(idUserAut)
        sql = sql + ")"
        sql = sql + " ORDER BY m.fecha"        
        #print(sql)
        self.cursor.execute(sql)
        ResQuery=self.cursor.fetchall()
        # Convertim data a string
        for valor in ResQuery:
            valor['fecha']=self.dataToString(valor['fecha'])
        return ResQuery

    def nouMissatge(self, idInterlocutor, idUserAut,missatge):
        sql = "INSERT INTO missatges (fecha, id_sender, id_receiver,"
        sql = sql + " missatge, status)"
        sql = sql + " VALUES (now(),'"+str(idUserAut)+"','"+str(idInterlocutor)+"',"
        sql = sql + " '"+missatge['text']+"', 'send')"
        # Executam sql mitjançant un try - except
        try:
            self.cursor.execute(sql)
            return ('Missatge enviat amb èxit')
        except:
            return ('Missatge NO enviat')
    
    def canviaStatusRebut(self, idUserAut):
        sql = "UPDATE missatges"
        sql = sql + " SET status='received'"
        sql = sql + " WHERE status='send'"
        sql = sql + " AND id_receiver="+str(idUserAut)
        # Executam sql mitjançant un try - except
        try:
            self.cursor.execute(sql)
            return ('Status modificat a REBUT')
        except:
            return ('Status NO modificat')
        
    def canviaStatusLlegit(self, idUserAut):
        sql = "UPDATE missatges"
        sql = sql + " SET status='read'"
        sql = sql + " WHERE status='received'"
        sql = sql + " AND id_receiver="+str(idUserAut)
        # Executam sql mitjançant un try - except
        try:
            self.cursor.execute(sql)
            return ('Status modificat a LLEGIT')
        except:
            return ('Status NO modificat')


#
# TASCA AVANÇADA
#

    def tornaGrups(self, idUserAut):
        sql = "SELECT g.id_grup, g.groupname"
        sql = sql + " FROM grups g"
        sql = sql + " JOIN members_grup m ON g.id_grup=m.id_grup"
        sql = sql + " WHERE m.id_member="+str(idUserAut)
        self.cursor.execute(sql)
        ResQuery=self.cursor.fetchall()
        if (ResQuery == ()):
            return('Aquest usuari no pertany a cap grup')
        else:
            return ResQuery
    
    def tornaGrups(self, idUserAut):
        sql = "SELECT g.id_grup, g.groupname"
        sql = sql + " FROM grups g"
        sql = sql + " JOIN members_grup m ON g.id_grup=m.id_grup"
        sql = sql + " WHERE m.id_member="+str(idUserAut)
        self.cursor.execute(sql)
        ResQuery=self.cursor.fetchall()
        if (ResQuery == ()):
            return('Aquest usuari no pertany a cap grup')
        else:
            return ResQuery

    def tornaMembresGrups(self, idUserAut):
        sql = "SELECT DISTINCT ub.id_user, ub.username, g.groupname"
        sql = sql + " FROM grups g"
        sql = sql + " INNER JOIN members_grup mg ON g.id_grup = mg.id_grup"
        sql = sql + " INNER JOIN users_base ub ON mg.id_member = ub.id_user"
        sql = sql + " WHERE g.id_grup IN (SELECT id_grup FROM members_grup"
        sql = sql + " WHERE id_member='"+str(idUserAut)+"')"
        self.cursor.execute(sql)
        ResQuery=self.cursor.fetchall()
        if (ResQuery == ()):
            return('Aquest usuari no pertany a cap grup')
        else:
            return ResQuery

    def tornaNumMissatgesGrup(self, idUserAut):
        sql = "SELECT g.groupname, COUNT(*) as num_messages_send"
        sql = sql + " FROM grups g"
        sql = sql + " JOIN members_grup mg ON g.id_grup = mg.id_grup"
        sql = sql + " JOIN missatges_grup mgp ON g.id_grup = mgp.id_receiver_grup"
        sql = sql + " JOIN estat_missatges_grup em ON mgp.id_missatge = em.id_missatge"
        sql = sql + " WHERE mg.id_member ='"+str(idUserAut)+"'"
        sql = sql + " AND em.status = 'send'"
        sql = sql + " AND em.id_receiver ='"+str(idUserAut)+"'"
        sql = sql + " GROUP BY g.groupname"
        self.cursor.execute(sql)
        ResQuery=self.cursor.fetchall()
        if (ResQuery == ()):
            return('Aquest usuari no pertany a cap grup')
        else:
            return ResQuery

    def tornaMissatgesConversaGrup(self, idGrup, idUserAut):
        sql = "SELECT grups.groupname, missatges_grup.id_missatge,"
        sql = sql + "  missatges_grup.data, missatges_grup.missatge,"
        sql = sql + "  users_base.username AS sender"
        sql = sql + " FROM grups"
        sql = sql + " INNER JOIN members_grup ON grups.id_grup=members_grup.id_grup"
        sql = sql + " INNER JOIN missatges_grup ON grups.id_grup=missatges_grup.id_receiver_grup"
        sql = sql + " INNER JOIN users_base ON missatges_grup.id_sender=users_base.id_user"
        sql = sql + " WHERE members_grup.id_member='"+str(idUserAut)+"'"
        sql = sql + " AND missatges_grup.id_receiver_grup='"+str(idGrup)+"'"
        sql = sql + " ORDER BY missatges_grup.data"
        print(sql)
        self.cursor.execute(sql)
        ResQuery=self.cursor.fetchall()
        if (ResQuery == ()):
            return('No hi ha missatges per mostrar')
        else:
            # Convertim data a string
            for valor in ResQuery:
                valor['data']=self.dataToString(valor['data'])
            return ResQuery

    def nouMissatgeGrup(self, idGrup, idUserAut,missatge):
        # Comprovam que existeix grup
        sql = "SELECT COUNT(id_grup) FROM grups"
        sql = sql + " WHERE id_grup="+str(idGrup)
        self.cursor.execute(sql)
        ResQuery=self.cursor.fetchone()
        if (ResQuery['COUNT(id_grup)'] == 1):
            # Comprovam que usuari autenticat pertany a grup
            sql = "SELECT COUNT(id_member) FROM members_grup"
            sql = sql + " WHERE id_grup='"+str(idGrup)+"'"
            sql = sql + " AND id_member="+str(idUserAut)            
            self.cursor.execute(sql)
            ResQuery=self.cursor.fetchone()
            if (ResQuery['COUNT(id_member)'] == 1):
                return ('Anam be')
            else:
                return ('Aquest usuari no pertaney a aquest grup de conversa')
        else:
            return ('Grup de conversa inexistent')
            
        """ sql = "INSERT INTO missatges (fecha, id_sender, id_receiver,"
        sql = sql + " missatge, status)"
        sql = sql + " VALUES (now(),'"+str(idUserAut)+"','"+str(idInterlocutor)+"',"
        sql = sql + " '"+missatge['text']+"', 'send')"
        # Executam sql mitjançant un try - except
        try:
            self.cursor.execute(sql)
            return ('Missatge enviat amb èxit')
        except:
            return ('Missatge NO enviat') """