import MySQLdb
host     = "localhost"
user     = "loja"
password = "loja0909!"
db       = "loja"
port     =  3306

conn = MySQLdb.connect(host, user, password, db, port)
cursor = conn.cursor()

cursor.execute("""
DELETE FROM funcionarios WHERE id > 0
""")