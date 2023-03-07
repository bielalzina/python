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

    def tornaUsername(self):
        sql = "SELECT username FROM users_base"
        self.cursor.execute(sql)
        ResQuery=self.cursor.fetchall()
        return ResQuery

    def autenticaUsuari(self):
        sql = "SELECT * FROM users_base "
        self.cursor.execute(sql)
        ResQuery=self.cursor.fetchall()
        print(ResQuery)
        return ResQuery