from con_version2 import *
import pymysql
import time

connectionn = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db='SRV1'
                             )
cursor = connectionn.cursor()

sql1 = 'INSERT INTO `SRV1_Ram` (`total`,`used`,`free`,`shared`,`buff_cache`,`available`,`Date`) VALUES (%s, %s, %s, %s, %s, %s, %s)'
sql2 = 'INSERT INTO `SRV1_Ram_actif` (`total`,`used`,`free`,`shared`,`buff_cache`,`available`,`Date`) VALUES (%s, %s, %s, %s, %s, %s, %s)'


def ram(password):
    cursor.execute("delete from SRV1_Ram_actif")
    T = connection("192.168.126.144", "root", password, 'free -hm')
    d = str(T).splitlines()
    l = []
    for i in d:
        p = str(i).split(" ")
        l = l + p
    a = ['', 'total', 'used', 'free', 'shared', 'buff/cache', 'available', 'Mem:', 'Swap:']
    b = []
    for i in range(len(l)):
        if l[i] not in a:
            b.append(l[i])
    t = time.gmtime()
    s = time.asctime(t)
    s = str(s)
    j = 0
    cursor.execute(sql1, (b[j], b[j+1], b[j+2], b[j+3], b[j+4], b[j+5], s))
    cursor.execute(sql2, (b[j], b[j+1], b[j+2], b[j+3], b[j+4], b[j+5], s))
    connectionn.commit()

