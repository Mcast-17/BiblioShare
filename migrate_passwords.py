import pymysql#Per connettere il database#
import bcrypt#Per creare hash sicuri delle password#

# connessione DB (uguale a Flask)#
db = pymysql.connect(
    host="localhost",
    user="root",
    password="TesiDatabase2026!",
    database="biblioteca_share",
    cursorclass=pymysql.cursors.DictCursor
)
#Creazione “cursore”, cioè l’oggetto che permette di:eseguire query SQL,leggere e modificare dati nel database#
cursor = db.cursor()

# tutti gli utenti#
cursor.execute("SELECT id_user, email, password FROM UTENTI")
#fetchall recupera i dati e li mette in dizionari#
utenti = cursor.fetchall()

for u in utenti:
    password = u["password"]#Estrae la password dell’utente corrente dal database#

    #Se NON è hashata Controlla se la password è già in formato bcrypt:le password hashate bcrypt iniziano con $2b$#
    #Se NON inizia così → significa che è ancora in chiaro#
    if not password.startswith("$2b$"):
    
    #Converte la password in chiaro in hash sicuro#
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

#Aggiorna il database:Sostituzione password in chiaro a password hashate#
        cursor.execute("""
            UPDATE UTENTI
            SET password = %s
            WHERE id_user = %s
        """, (hashed, u["id_user"]))
        
#Messaggio di log:stampa a schermo quale utente è stato aggiornato,utile per controllare il processo#
        print(f"Password migrata per {u['email']}")

db.commit()#Conferma tutte le modifiche nel database:senza questo non vengono salvate le modifiche#
db.close()#Chiude la connessione al database#

print("Migrazione completata")#Messaggio finale che indica:tutte le password sono state convertite con successo#