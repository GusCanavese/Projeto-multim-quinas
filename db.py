import MySQLdb
# host     = "ballast.proxy.rlwy.net"
# user     = "root"
# password = "cUxQKiTNIHZUlBQhphYhiESVTcrCJTGO"
# db       = "loja"
# port     =  15192
host     = "localhost"
user     = "loja"
password = "loja0909!"
db       = "loja"
port     =  3306

conn = MySQLdb.connect(host, user, password, db, port)
cursor = conn.cursor()

# cursor.execute("""
# DROP table teste
# """)mysql://root:cUxQKiTNIHZUlBQhphYhiESVTcrCJTGO@ballast.proxy.rlwy.net:15192/railway
# mysql://root:cUxQKiTNIHZUlBQhphYhiESVTcrCJTGO@mysql.railway.internal:3306/railway