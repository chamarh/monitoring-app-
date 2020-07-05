from con_version2 import *
import pymysql
import time

connectionn = pymysql.connect(host='localhost',
                              user='root',
                              password='',
                              db='SRV1'
                              )
cursor = connectionn.cursor()

sql1 = "INSERT INTO `SRV1_disque` (`name`, `size`, `used`, `avail`, `use_per`, `monted_on`, `Date`) VALUES (%s, %s, %s, %s, %s, %s, %s)"
sql2 = "INSERT INTO `SRV1_disque_actif` (`name`, `size`, `used`, `avail`, `use_per`, `monted_on`, `Date`) VALUES (%s, %s, %s, %s, %s, %s, %s)"


def memoire(password):
    cursor.execute("delete from SRV1_disque_actif")
    T = connection("192.168.126.144", "root", password, 'df -h')
    d = str(T).splitlines()
    l = []
    for i in d:
        p = str(i).split(" ")
        l = l + p
    a = ['', 'Filesystem', 'Size', 'Used', 'Avail', 'Use%', 'Mounted', 'on']
    b = []
    for i in range(len(l)):
        if l[i] not in a:
            b.append(l[i])

    t = time.gmtime()
    s = time.asctime(t)
    s = str(s)
    j = 0
    while j < len(b):
        cursor.execute(sql1, (b[j], b[j+1], b[j+2], b[j+3], b[j+4], b[j+5], s))
        cursor.execute(sql2, (b[j], b[j+1], b[j+2], b[j+3], b[j+4], b[j+5], s))
        connectionn.commit()
        j = j+6

