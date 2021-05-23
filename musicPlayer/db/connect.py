import MySQLdb

def connection():
    conn = MySQLdb.connect(host="localhost",
                           user = "root",
                           passwd = "password",
                           db = "music_player")
    c = conn.cursor()
    return c, conn