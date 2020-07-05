from users import *
from memoire import *
from ram import *
from getpass import getpass

password = getpass()

while True:
    user(password)
    memoire(password)
    ram(password)
    time.sleep(30)

