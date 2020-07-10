from flask import *
import time
from datetime import timedelta
import hashlib
import logging
from Database.database_connection import *
from livereload import Server
from Servers.SSH_connexion_to_servers import *
#################################################
logging.basicConfig(filename='activity.log',level=logging.DEBUG,format='%(levelname)s %(asctime)s %(message)s',datefmt="%m/%d/%Y %I:%M:%S %p")
#################################################
app = Flask(__name__)
app.secret_key = 'thisismysecretkey'
#################################################
@app.before_request
def before_request():
    app.permanent_session_lifetime = timedelta(minutes=20)
    g.username = None
    if 'username' in session :
        g.username = session['username']
#################################################
@app.route('/login',methods=['POST',"GET"])
def login():
    if request.method == "POST" :
        session.pop('username',None)
        cursor = connection.cursor()
        cursor.execute('select * from Administrators')
        data = cursor.fetchall()
        objectHash = hashlib.sha256(str(request.form["password"]).encode('utf-8'))
        hashed_password = objectHash.hexdigest()
        for person in data:
            if person[0] == request.form["email"] and person[1] == hashed_password :
                session['username']= person[3]+" "+person[2]
                session.permanent = True
                message = "Successful connexion from "+request.form["email"]+" using IP : "+request.environ['REMOTE_ADDR']
                logging.info(message)
                return redirect('/home')
            else :
                flash("Your credentials are incorrect. Please retry")
                return redirect("/login")
        message = "Failed connexion from "+request.form["email"]+" using IP : "+request.environ['REMOTE_ADDR']
        logging.warning(message)
        return redirect('/login')
    return render_template("login.html")
#################################################
@app.route("/logout",methods=["GET"])
def logout():
    session.pop('username',None)
    flash("Logged out successfully !")
    return redirect("/login")
#################################################
@app.route('/home',methods=['GET','POST'])
def home():
    if g.username :
       return render_template("homepage.html",username=session['username'])
    return redirect("/login")
################################################
actions = ['supervise1','supervise2','supervise3','manage1','manage2','manage3']
@app.route("/home/<action>",methods=["GET"])
def supervise_server(action):
    if str(action) in actions :
        Htmlfile = str(action) + ".html"
        return render_template(Htmlfile,username=session['username'])
    return "Page Not Found"
################################################
@app.route("/home/supervise1/active_users",methods=["GET"])
def supervise1_active_users():
    while True :
        connection = pymysql.connect(host='localhost',
                                     user='mc21',
                                     password='root',
                                     db='Admin')
        cursor2 = connection.cursor()
        sql = "select distinct * from SRV1_users_actif"
        cursor2.execute(sql)
        bigdata = cursor2.fetchall()
        return render_template("SRV1_active_users.html", data=bigdata, username=session["username"])
################################################
@app.route("/home/supervise2/active_users",methods=["GET"])
def supervise2_active_users():
    while True :
        connection = pymysql.connect(host='localhost',
                                     user='mc21',
                                     password='root',
                                     db='Admin')
        cursor2 = connection.cursor()
        sql = "select distinct * from SRV2_users_actif"
        cursor2.execute(sql)
        bigdata = cursor2.fetchall()
        return render_template("SRV2_active_users.html", data=bigdata, username=session["username"])
################################################
@app.route("/home/supervise3/active_users",methods=["GET"])
def supervise3_active_users():
    while True :
        connection = pymysql.connect(host='localhost',
                                     user='mc21',
                                     password='root',
                                     db='Admin')
        cursor2 = connection.cursor()
        sql = "select distinct * from SRV3_users_actif"
        cursor2.execute(sql)
        bigdata = cursor2.fetchall()
        return render_template("SRV3_active_users.html", data=bigdata, username=session["username"])
################################################
@app.route("/home/supervise1/ram_usage",methods=["GET"])
def supervise1_ram_usage():
    while True :
        connection = pymysql.connect(host='localhost',
                                     user='mc21',
                                     password='root',
                                     db='Admin')
        cursor2 = connection.cursor()
        sql = "select * from SRV1_ram_actif"
        cursor2.execute(sql)
        bigdata = cursor2.fetchall()
        return render_template("SRV1_active_ram_usage.html", data=bigdata, username=session["username"])
        time.sleep(2)
################################################
@app.route("/home/supervise2/ram_usage",methods=["GET"])
def supervise2_ram_usage():
    while True :
        connection = pymysql.connect(host='localhost',
                                     user='mc21',
                                     password='root',
                                     db='Admin')
        cursor2 = connection.cursor()
        sql = "select * from SRV2_ram_actif"
        cursor2.execute(sql)
        bigdata = cursor2.fetchall()
        return render_template("SRV2_active_ram_usage.html", data=bigdata, username=session["username"])
        time.sleep(2)
################################################
@app.route("/home/supervise3/ram_usage",methods=["GET"])
def supervise3_ram_usage():
    while True :
        connection = pymysql.connect(host='localhost',
                                     user='mc21',
                                     password='root',
                                     db='Admin')
        cursor2 = connection.cursor()
        sql = "select * from SRV3_ram_actif"
        cursor2.execute(sql)
        bigdata = cursor2.fetchall()
        return render_template("SRV3_active_ram_usage.html", data=bigdata, username=session["username"])
        time.sleep(2)
################################################
@app.route("/home/supervise1/hard_drive_usage",methods=["GET"])
def supervise1_disk_usage():
    while True :
        connection = pymysql.connect(host='localhost',
                                     user='mc21',
                                     password='root',
                                     db='Admin')
        cursor2 = connection.cursor()
        sql = "select * from SRV1_disk_actif"
        cursor2.execute(sql)
        bigdata = cursor2.fetchall()
        return render_template("SRV1_active_disk_usage.html", data=bigdata, username=session["username"])
        time.sleep(3)
################################################
@app.route("/home/supervise2/hard_drive_usage",methods=["GET"])
def supervise2_disk_usage():
    while True :
        connection = pymysql.connect(host='localhost',
                                     user='mc21',
                                     password='root',
                                     db='Admin')
        cursor2 = connection.cursor()
        sql = "select * from SRV2_disk_actif"
        cursor2.execute(sql)
        bigdata = cursor2.fetchall()
        return render_template("SRV2_active_disk_usage.html", data=bigdata, username=session["username"])
        time.sleep(3)
################################################
@app.route("/home/supervise3/hard_drive_usage",methods=["GET"])
def supervise3_disk_usage():
    while True :
        connection = pymysql.connect(host='localhost',
                                     user='mc21',
                                     password='root',
                                     db='Admin')
        cursor2 = connection.cursor()
        sql = "select * from SRV3_disk_actif"
        cursor2.execute(sql)
        bigdata = cursor2.fetchall()
        return render_template("SRV3_active_disk_usage.html", data=bigdata, username=session["username"])
        time.sleep(3)
################################################
@app.route("/home/manage1/add",methods=["GET","POST"])
def manage1_useradd():
    if request.method == "POST":
        useradd = "useradd "
        if request.form["user_id"] != '' :
            useradd += "-u "+str(request.form["user_id"])+" "
        if request.form["group_name"] != '' :
            useradd += "-g "+str(request.form["group_name"])+" "
        if request.form["directory"] != '' :
            create_directory = "mkdir "+str(request.form.get("parent_directory_selection"))+str(request.form["directory"])
            execution = connect_SRV1.send_command(create_directory)
            useradd += "-d "+str(request.form.get("parent_directory_selection"))+str(request.form["directory"])+" "
        if request.form.get("shell_selection") != None :
            useradd += " -s "+str(request.form.get("shell_selection"))+" "
        useradd += request.form["username"]
        commit = connect_SRV1.send_command(useradd)
        if commit == '' :
            flash("User added successfully")
        error1 = "useradd: user '{}' already exists".format(str(request.form["username"]))
        error2 = "useradd: UID "+str(request.form["user_id"])+" is not unique"
        error3 = "useradd: group '{}' does not exist".format(request.form["group_name"])
        if commit == error1:
            alert = "User "+str(request.form["username"])+" already exists"
            flash(alert)
        if commit == error2 :
            alert = "User ID "+str(request.form["user_id"])+" already exists"
            flash(alert)
        if commit == error3 :
            alert = "Group "+str(request.form["group_name"])+" does not exist"
            flash(alert)
        return redirect("/home/manage1/add")
    return render_template("SRV1_useradd.html", username=session["username"])
################################################
@app.route("/home/manage2/add",methods=["GET","POST"])
def manage2_useradd():
    if request.method == "POST":
        useradd = "useradd "
        if request.form["user_id"] != '' :
            useradd += "-u "+str(request.form["user_id"])+" "
        if request.form["group_name"] != '' :
            useradd += "-g "+str(request.form["group_name"])+" "
        if request.form["directory"] != '' :
            create_directory = "mkdir "+str(request.form.get("parent_directory_selection"))+str(request.form["directory"])
            execution = connect_SRV2.send_command(create_directory)
            useradd += "-d "+str(request.form.get("parent_directory_selection"))+str(request.form["directory"])+" "
        if request.form.get("shell_selection") != None :
            useradd += " -s "+str(request.form.get("shell_selection"))+" "
        useradd += request.form["username"]
        commit = connect_SRV2.send_command(useradd)
        if commit == '' :
            flash("User added successfully")
        error1 = "useradd: user '{}' already exists".format(str(request.form["username"]))
        error2 = "useradd: UID "+str(request.form["user_id"])+" is not unique"
        error3 = "useradd: group '{}' does not exist".format(request.form["group_name"])
        if commit == error1:
            alert = "User "+str(request.form["username"])+" already exists"
            flash(alert)
        if commit == error2 :
            alert = "User ID "+str(request.form["user_id"])+" already exists"
            flash(alert)
        if commit == error3 :
            alert = "Group "+str(request.form["group_name"])+" does not exist"
            flash(alert)
        return redirect("/home/manage2/add")
    return render_template("SRV2_useradd.html", username=session["username"])
################################################
@app.route("/home/manage3/add",methods=["GET","POST"])
def manage3_useradd():
    if request.method == "POST":
        useradd = "useradd "
        if request.form["user_id"] != '' :
            useradd += "-u "+str(request.form["user_id"])+" "
        if request.form["group_name"] != '' :
            useradd += "-g "+str(request.form["group_name"])+" "
        if request.form["directory"] != '' :
            create_directory = "mkdir "+str(request.form.get("parent_directory_selection"))+str(request.form["directory"])
            execution = connect_SRV3.send_command(create_directory)
            useradd += "-d "+str(request.form.get("parent_directory_selection"))+str(request.form["directory"])+" "
        if request.form.get("shell_selection") != None :
            useradd += " -s "+str(request.form.get("shell_selection"))+" "
        useradd += request.form["username"]
        commit = connect_SRV3.send_command(useradd)
        if commit == '' :
            flash("User added successfully")
        error1 = "useradd: user '{}' already exists".format(str(request.form["username"]))
        error2 = "useradd: UID "+str(request.form["user_id"])+" is not unique"
        error3 = "useradd: group '{}' does not exist".format(request.form["group_name"])
        if commit == error1:
            alert = "User "+str(request.form["username"])+" already exists"
            flash(alert)
        if commit == error2 :
            alert = "User ID "+str(request.form["user_id"])+" already exists"
            flash(alert)
        if commit == error3 :
            alert = "Group "+str(request.form["group_name"])+" does not exist"
            flash(alert)
        return redirect("/home/manage3/add")
    return render_template("SRV3_useradd.html", username=session["username"])
################################################
@app.route("/home/manage1/delete",methods=["GET","POST"])
def manage1_userdel():
    if request.method == "POST":
        if request.form["username"] == "root" :
            flash("Operation dismissed. You can't delete root account! ")
        userdel = "userdel "
        userdel += str(request.form["username"])
        execution = connect_SRV1.send_command(userdel)
        error = "userdel: user '{}' does not exist".format(request.form["username"])
        if True :
            if execution == error :
                alert = "User " + str(request.form["username"]) + " does not exist"
                flash(alert)
            else :
                flash("User deleted successfully")
        return  redirect("/home/manage1/delete")
    return render_template("SRV1_userdel.html", username=session["username"])
################################################
@app.route("/home/manage2/delete",methods=["GET","POST"])
def manage2_userdel():
    if request.method == "POST":
        if request.form["username"] == "root" :
            flash("Operation dismissed. You can't delete root account! ")
        userdel = "userdel "
        userdel += str(request.form["username"])
        execution = connect_SRV2.send_command(userdel)
        error = "userdel: user '{}' does not exist".format(request.form["username"])
        if True :
            if execution == error :
                alert = "User " + str(request.form["username"]) + " does not exist"
                flash(alert)
            else :
                flash("User deleted successfully")
        return  redirect("/home/manage2/delete")
    return render_template("SRV2_userdel.html", username=session["username"])
################################################
@app.route("/home/manage3/delete",methods=["GET","POST"])
def manage3_userdel():
    if request.method == "POST":
        if request.form["username"] == "root" :
            flash("Operation dismissed. You can't delete root account! ")
        userdel = "userdel "
        userdel += str(request.form["username"])
        execution = connect_SRV3.send_command(userdel)
        error = "userdel: user '{}' does not exist".format(request.form["username"])
        if True :
            if execution == error :
                alert = "User " + str(request.form["username"]) + " does not exist"
                flash(alert)
            else :
                flash("User deleted successfully")
        return  redirect("/home/manage3/delete")
    return render_template("SRV3_userdel.html", username=session["username"])
################################################
@app.route("/home/manage1/password",methods=["GET","POST"])
def manage1_password():
    if request.method == "POST":
        locked=False
        unlocked=False
        deleted=False
        password = "passwd "
        if request.form.get("choice") == "lock":
            password += "-l "
            locked = True
        if request.form.get("choice") == "unlock":
            password += "-u "
            unlocked = True
        if request.form.get("choice") == "delete":
            password += "-d "
            deleted = True
        password += request.form["username"]
        execution = connect_SRV1.send_command(password)
        error = "passwd: user '{}' does not exist".format(request.form["username"])
        if True :
            if execution == error :
                alert = "User " + str(request.form["username"]) + " does not exist"
                flash(alert)
                return redirect("/home/manage1/password")
            if locked:
                flash("Account locked successfully")
                return redirect("/home/manage1/password")
            if unlocked :
                flash("Account unlocked successfully")
                return redirect("/home/manage1/password")
            if deleted :
                flash("Password removed successfully")
                return redirect("/home/manage1/password")
    return render_template("SRV1_password.html", username=session["username"])
################################################
@app.route("/home/manage2/password",methods=["GET","POST"])
def manage2_password():
    if request.method == "POST":
        locked=False
        unlocked=False
        deleted=False
        password = "passwd "
        if request.form.get("choice") == "lock":
            password += "-l "
            locked = True
        if request.form.get("choice") == "unlock":
            password += "-u "
            unlocked = True
        if request.form.get("choice") == "delete":
            password += "-d "
            deleted = True
        password += request.form["username"]
        execution = connect_SRV2.send_command(password)
        error = "passwd: user '{}' does not exist".format(request.form["username"])
        if True :
            if execution == error :
                alert = "User " + str(request.form["username"]) + " does not exist"
                flash(alert)
                return redirect("/home/manage2/password")
            if locked:
                flash("Account locked successfully")
                return redirect("/home/manage2/password")
            if unlocked :
                flash("Account unlocked successfully")
                return redirect("/home/manage2/password")
            if deleted :
                flash("Password removed successfully")
                return redirect("/home/manage2/password")
    return render_template("SRV2_password.html", username=session["username"])
################################################
@app.route("/home/manage3/password",methods=["GET","POST"])
def manage3_password():
    if request.method == "POST":
        locked=False
        unlocked=False
        deleted=False
        password = "passwd "
        if request.form.get("choice") == "lock":
            password += "-l "
            locked = True
        if request.form.get("choice") == "unlock":
            password += "-u "
            unlocked = True
        if request.form.get("choice") == "delete":
            password += "-d "
            deleted = True
        password += request.form["username"]
        execution = connect_SRV3.send_command(password)
        error = "passwd: user '{}' does not exist".format(request.form["username"])
        if True :
            if execution == error :
                alert = "User " + str(request.form["username"]) + " does not exist"
                flash(alert)
                return redirect("/home/manage3/password")
            if locked:
                flash("Account locked successfully")
                return redirect("/home/manage3/password")
            if unlocked :
                flash("Account unlocked successfully")
                return redirect("/home/manage3/password")
            if deleted :
                flash("Password removed successfully")
                return redirect("/home/manage3/password")
    return render_template("SRV3_password.html", username=session["username"])
################################################
@app.route("/home/manage1/services",methods=["GET","POST"])
def manage1_services():
    if request.method == "POST":
        start   = False
        stop    = False
        restart = False
        service = "systemctl "
        if request.form["submit_button"]== "start" :
            service += "start "
            start = True
        if request.form["submit_button"] == "stop":
            service += "stop "
            stop = True
        if request.form["submit_button"] == "restart":
            service += "restart "
            restart = True
        service += request.form["service"]
        execution = connect_SRV1.send_command(service)
        if True :
            if execution == '' :
                if start :
                    flash("Service started successfully")
                    return redirect("/home/manage1/services")
                if stop :
                    flash("Service stopped successfully")
                    return redirect("/home/manage1/services")
                if restart :
                    flash("Service restarted successfully")
                    return redirect("/home/manage1/services")
            else:
                flash(execution)
                return redirect("/home/manage1/services")
    return render_template("SRV1_services.html", username=session["username"])
################################################
@app.route("/home/manage2/services",methods=["GET","POST"])
def manage2_services():
    if request.method == "POST":
        start   = False
        stop    = False
        restart = False
        service = "systemctl "
        if request.form["submit_button"]== "start" :
            service += "start "
            start = True
        if request.form["submit_button"] == "stop":
            service += "stop "
            stop = True
        if request.form["submit_button"] == "restart":
            service += "restart "
            restart = True
        service += request.form["service"]
        execution = connect_SRV2.send_command(service)
        if True :
            if execution == '' :
                if start :
                    flash("Service started successfully")
                    return redirect("/home/manage2/services")
                if stop :
                    flash("Service stopped successfully")
                    return redirect("/home/manage2/services")
                if restart :
                    flash("Service restarted successfully")
                    return redirect("/home/manage2/services")
            else:
                flash(execution)
                return redirect("/home/manage2/services")
    return render_template("SRV2_services.html", username=session["username"])
################################################
@app.route("/home/manage3/services",methods=["GET","POST"])
def manage3_services():
    if request.method == "POST":
        start   = False
        stop    = False
        restart = False
        service = "systemctl "
        if request.form["submit_button"]== "start" :
            service += "start "
            start = True
        if request.form["submit_button"] == "stop":
            service += "stop "
            stop = True
        if request.form["submit_button"] == "restart":
            service += "restart "
            restart = True
        service += request.form["service"]
        execution = connect_SRV3.send_command(service)
        if True :
            if execution == '' :
                if start :
                    flash("Service started successfully")
                    return redirect("/home/manage3/services")
                if stop :
                    flash("Service stopped successfully")
                    return redirect("/home/manage3/services")
                if restart :
                    flash("Service restarted successfully")
                    return redirect("/home/manage3/services")
            else:
                flash(execution)
                return redirect("/home/manage3/services")
    return render_template("SRV3_services.html", username=session["username"])
################################################
@app.route("/home/manage1/groupadd",methods=["GET","POST"])
def manage1_groupadd():
    if request.method == "POST" :
        grouppadd = "groupadd "
        if request.form["group_id"] != '':
            grouppadd += "-g "+request.form["group_id"]+" "
        grouppadd += request.form["groupname"]
        execution = connect_SRV1.send_command(grouppadd)
        error1 = "groupadd: group '{}' already exists".format(str(request.form["groupname"]))
        error2 = "groupadd: GID '{}' already exists".format(str(request.form["group_id"]))
        if True :
            if execution == '':
                flash("Group added successfully")
                return redirect("/home/manage1/groupadd")
            if execution == error1 :
                flash("Group name already exists. Retry !")
                return redirect("/home/manage1/groupadd")
            if execution == error2 :
                flash("Group ID already exists. Retry !")
                return redirect("/home/manage1/groupadd")
            else:
                flash(execution)
                return redirect("/home/manage1/groupadd")
    return render_template("SRV1_groupadd.html", username=session["username"])
################################################
@app.route("/home/manage2/groupadd",methods=["GET","POST"])
def manage2_groupadd():
    if request.method == "POST" :
        grouppadd = "groupadd "
        if request.form["group_id"] != '':
            grouppadd += "-g "+request.form["group_id"]+" "
        grouppadd += request.form["groupname"]
        execution = connect_SRV2.send_command(grouppadd)
        error1 = "groupadd: group '{}' already exists".format(str(request.form["groupname"]))
        error2 = "groupadd: GID '{}' already exists".format(str(request.form["group_id"]))
        if True :
            if execution == '':
                flash("Group added successfully")
                return redirect("/home/manage2/groupadd")
            if execution == error1 :
                flash("Group name already exists. Retry !")
                return redirect("/home/manage2/groupadd")
            if execution == error2 :
                flash("Group ID already exists. Retry !")
                return redirect("/home/manage2/groupadd")
            else:
                flash(execution)
                return redirect("/home/manage2/groupadd")
    return render_template("SRV2_groupadd.html", username=session["username"])
################################################
@app.route("/home/manage3/groupadd",methods=["GET","POST"])
def manage3_groupadd():
    if request.method == "POST" :
        grouppadd = "groupadd "
        if request.form["group_id"] != '':
            grouppadd += "-g "+request.form["group_id"]+" "
        grouppadd += request.form["groupname"]
        execution = connect_SRV3.send_command(grouppadd)
        error1 = "groupadd: group '{}' already exists".format(str(request.form["groupname"]))
        error2 = "groupadd: GID '{}' already exists".format(str(request.form["group_id"]))
        if True :
            if execution == '':
                flash("Group added successfully")
                return redirect("/home/manage3/groupadd")
            if execution == error1 :
                flash("Group name already exists. Retry !")
                return redirect("/home/manage3/groupadd")
            if execution == error2 :
                flash("Group ID already exists. Retry !")
                return redirect("/home/manage3/groupadd")
            else:
                flash(execution)
                return redirect("/home/manage3/groupadd")
    return render_template("SRV3_groupadd.html", username=session["username"])
################################################
@app.route("/home/manage1/groupdel",methods=["GET","POST"])
def manage1_groupdel():
    if request.method == "POST" :
        groupdel = "groupdel "+request.form["groupname"]
        execution = connect_SRV1.send_command(groupdel)
        if True:
            if execution == '' :
                flash("Group deleted successfully")
                return redirect("/home/manage1/groupdel")
            else :
                flash(execution)
                return  redirect("/home/manage1/groupdel")
    return render_template("SRV1_groupdel.html", username=session["username"])
################################################
@app.route("/home/manage2/groupdel",methods=["GET","POST"])
def manage2_groupdel():
    if request.method == "POST" :
        groupdel = "groupdel "+request.form["groupname"]
        execution = connect_SRV2.send_command(groupdel)
        if True:
            if execution == '' :
                flash("Group deleted successfully")
                return redirect("/home/manage2/groupdel")
            else :
                flash(execution)
                return  redirect("/home/manage2/groupdel")
    return render_template("SRV2_groupdel.html", username=session["username"])
################################################
@app.route("/home/manage3/groupdel",methods=["GET","POST"])
def manage3_groupdel():
    if request.method == "POST" :
        groupdel = "groupdel "+request.form["groupname"]
        execution = connect_SRV3.send_command(groupdel)
        if True:
            if execution == '' :
                flash("Group deleted successfully")
                return redirect("/home/manage3/groupdel")
            else :
                flash(execution)
                return  redirect("/home/manage3/groupdel")
    return render_template("SRV3_groupdel.html", username=session["username"])
################################################
@app.route("/home/supervise1/connexion_history",methods=["GET"])
def SRV1_connexion_history():
    connection = pymysql.connect(host='localhost',
                                 user='mc21',
                                 password='root',
                                 db='Admin')
    cursor2 = connection.cursor()
    sql = "select * from SRV1_users"
    cursor2.execute(sql)
    bigdata = cursor2.fetchall()
    return render_template("SRV1_connexion_history.html", username=session["username"], data=bigdata)
################################################
@app.route("/home/supervise2/connexion_history",methods=["GET"])
def SRV2_connexion_history():
    connection = pymysql.connect(host='localhost',
                                 user='mc21',
                                 password='root',
                                 db='Admin')
    cursor2 = connection.cursor()
    sql = "select * from SRV2_users"
    cursor2.execute(sql)
    bigdata = cursor2.fetchall()
    return render_template("SRV2_connexion_history.html", username=session["username"], data=bigdata)
################################################
@app.route("/home/supervise3/connexion_history",methods=["GET"])
def SRV3_connexion_history():
    connection = pymysql.connect(host='localhost',
                                 user='mc21',
                                 password='root',
                                 db='Admin')
    cursor2 = connection.cursor()
    sql = "select * from SRV3_users"
    cursor2.execute(sql)
    bigdata = cursor2.fetchall()
    return render_template("SRV3_connexion_history.html", username=session["username"], data=bigdata)
################################################
@app.route("/home/change_password",methods=["POST","GET"])
def change_password():
    if request.method == "POST" :
        T=str(session["username"]).split(" ")
        nom = T[1]
        prenom = T[0]
        if request.form["old_password"] == request.form["new_password"] :
            flash("Please set a different password than the old one")
            return redirect("/home/change_password")
        oldHash = hashlib.sha256(str(request.form["old_password"]).encode('utf-8'))
        hashed_old_password = oldHash.hexdigest()
        newHash = hashlib.sha256(str(request.form["new_password"]).encode('utf-8'))
        hashed_new_password = newHash.hexdigest()
        cursor.execute("select password from Administrators where nom = %s and prenom =%s",(nom,prenom))
        password_in_DB = cursor.fetchall()
        if True :
            if password_in_DB[0][0] == hashed_old_password :
                values = (hashed_new_password, nom, prenom)
                sql = "update Administrators set password = %s where nom = %s and prenom = %s"
                cursor.execute(sql,values)
                connection.commit()
                flash("Password updated successfully")
                return redirect("/home/change_password")
            else:
                flash("Your old password is incorrect")
                return  redirect("/home/change_password")
        return redirect("/home/change_password")
    return render_template("change_password.html",username=session["username"])
################################################
@app.route("/home/add_admin",methods=["POST","GET"])
def add_admin():
    if request.method == "POST" :
        Hash = hashlib.sha256(str(request.form["password"]).encode('utf-8'))
        hashed_password = Hash.hexdigest()
        sql = "insert into Administrators(email,password,nom,prenom) values (%s,%s,%s,%s)"
        v = (request.form["email"],hashed_password,request.form["admin_nom"],request.form["admin_prenom"])
        cursor.execute(sql,v)
        connection.commit()
        flash("Administrator added successfully")
        return redirect("/home/add_admin")
    return render_template("add_admin.html",username=session["username"])
################################################
if __name__ ==  "__main__" :
    server=Server(app.wsgi_app)
    server.serve()
    app.run(debug=True)

