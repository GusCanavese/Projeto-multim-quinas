import MySQLdb
host     = "ballast.proxy.rlwy.net"
user     = "root"
password = "cUxQKiTNIHZUlBQhphYhiESVTcrCJTGO"
db       = "loja"
port     =  15192


conn = MySQLdb.connect(host, user, password, db, port)
cursor = conn.cursor()
