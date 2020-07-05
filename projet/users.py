from con_version2 import *
import time
import pymysql

connectionn = pymysql.connect(host='localhost',
                              user='root',
                              password='',
                              db='SRV1'
                              )

cursor = connectionn.cursor()
sql1 = "INSERT INTO `SRV1_users` (`Username`, `Date`) VALUES (%s, %s)"
sql2 = "INSERT INTO `SRV1_users_actif` (`Username`, `Date`) VALUES (%s, %s)"

def user(password):
    cursor.execute("delete from SRV1_users_actif")
    T = connection("192.168.126.144", "root", password, 'users')
    T = str(T).split(" ")
    t = time.gmtime()
    s = time.asctime(t)
    s = str(s)
    for username in T:
        cursor.execute(sql1, (username, s))
        cursor.execute(sql2, (username, s))
        connectionn.commit()
