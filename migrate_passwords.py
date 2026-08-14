import os
import pymysql  # Per connettere il database
import bcrypt   # Per creare hash sicuri delle password
from dotenv import load_dotenv

# Carica le variabili dal file .env
load_dotenv()

# Recupero configurazione database
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# Connessione DB
db = pymysql.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME,
    cursorclass=pymysql.cursors.DictCursor
)

# Creazione cursore
# Permette di eseguire query SQL e leggere/modificare i dati
cursor = db.cursor()

# Recupera tutti gli utenti
cursor.execute("SELECT id_user, email, password FROM UTENTI")

# fetchall recupera i dati e li mette in dizionari
utenti = cursor.fetchall()

for u in utenti:

    # Estrae la password dell'utente corrente
    password = u["password"]

    # Controlla se la password è già hashata con bcrypt.
    # Le password bcrypt iniziano con $2b$
    if not password.startswith("$2b$"):

        # Converte la password in chiaro in un hash sicuro
        hashed = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

        # Aggiorna il database sostituendo
        # la password in chiaro con quella hashata
        cursor.execute("""
            UPDATE UTENTI
            SET password = %s
            WHERE id_user = %s
        """, (
            hashed,
            u["id_user"]
        ))

        # Messaggio di log
        print(f"Password migrata per {u['email']}")

# Conferma tutte le modifiche
db.commit()

# Chiude la connessione
db.close()

print("Migrazione completata")
