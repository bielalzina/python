import pymysql.cursors


class User():
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __str__(self):
        return f"User ID: {self.id}"


def tornaUsuaris():
    db = pymysql.connect(host='localhost',
                         user='root',
                         db='whatspauUT6repas',
                         charset='utf8mb4',
                         autocommit=True,
                         cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()
    sql = "SELECT * FROM users_base"
    cursor.execute(sql)
    ResQuery = cursor.fetchall()
    usuaris = []
    for row in ResQuery:
        usuaris.append(User(row['id_user'],
                       row['username'],
                       row['password']))
    db.close()
    print(usuaris)
    return usuaris
