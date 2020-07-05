from flask import *
from datetime import timedelta
import hashlib
from Database.database_connection import *

app = Flask(__name__)
app.secret_key = 'thisismysecretkey'   ## pour les sessions

#################################################
@app.before_request
def before_request():
    app.permanent_session_lifetime = timedelta(minutes=5)    ##  Session for lives 5 minutes after a recent request (Activity of admin)
    g.username = None                                        ## sessions
    if 'username' in session :                               ## sessions
        g.username = session['username']                     ## sessions
#################################################



@app.route('/login',methods=['POST',"GET"])
def login():
    if request.method == "POST" :  ## si l'admin essay
        session.pop('username',None)
        cursor = connection.cursor()
        cursor.execute('select * from Administrators')
        data = cursor.fetchall()    ## recevoire les donnees sous forme de tuples
        objectHash = hashlib.sha256(str(request.form["password"]).encode('utf-8'))
        hashed_password = objectHash.hexdigest()
        for person in data: ## parcours des donnees dans la tables Administrators qui contient email,passwd... des admin qui ont le droit de se connecter
            if person[0] == request.form["email"] and person[1] == hashed_password : ## verifier si les donnees saisies (email-password) existent dans la table Administrators
                session['username']= person[3]+" "+person[2] ## Configurer une session pour maintenir la connexion au site
                session.permanent = True ## Rendre la session permanante (mais on l'a limitee a 5 minutes dans la fonction before_request dans la ligne 11)
                return redirect('/home')  ## si les donnees sont correctes , l'admin est envoyer vers la route localhost:5000/home qu'on a definit au dessous
        ## On peut faire ici un traitement pour que si les info saisies sont incorrectes , on les ajoute dans un fichier log pour voir l'activite sur notre App
        return redirect('/login')  ## renvoyer vers la page de login a nouveau lorsque les email/passwd sont incorrectes
    return render_template("login.html")  ## si la methode n'est pas POST (donc GET) , on va afficher la page login.html
#################################################



@app.route("/logout",methods=["GET"])  ## cette route est appelee lorsqu'on clique sur le boutton 'logout' est donc on va supprimer la session (cad session['username'] va devenir = None)
def logout():
    session.pop('username',None) ## ceci est fait grace a la fonction pop()
    return redirect("/login")    ## apres suppression de la session , on redirige vers page de login pour inserer a nouveau lemail et passwd
#################################################




@app.route('/home',methods=['GET','POST'])
def home():
    if g.username :
       return render_template("homepage.html",username=session['username'])
    return redirect("/login")
################################################
