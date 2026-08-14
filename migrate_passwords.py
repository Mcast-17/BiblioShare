import os
import pymysql
import bcrypt
from dotenv import load_dotenv


# ============================================================
# CONFIGURAZIONE
# ============================================================

# Cartella principale di BiblioShare
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Il file .env si trova nella cartella app
ENV_FILE = os.path.join(BASE_DIR, "app", ".env")

# Carica le variabili dal file .env
load_dotenv(ENV_FILE)


# ============================================================
# CONFIGURAZIONE DATABASE
# ============================================================

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME", "biblioteca_share")


# Controllo che la password sia stata caricata
if not DB_PASSWORD:
    raise RuntimeError(
        f"DB_PASSWORD non trovata nel file .env: {ENV_FILE}"
    )


# ============================================================
# CONNESSIONE AL DATABASE
# ============================================================

db = None
cursor = None

try:

    print("==============================================")
    print("       MIGRAZIONE PASSWORD BIBLIOSHARE")
    print("==============================================")
    print()

    print("Connessione al database...")

    db = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )

    cursor = db.cursor()

    print("Connessione effettuata.")
    print()


    # ========================================================
    # RECUPERO DI TUTTI GLI UTENTI
    # ========================================================

    cursor.execute("""
        SELECT id_user, email, password
        FROM UTENTI
    """)

    utenti = cursor.fetchall()

    print(f"Utenti trovati: {len(utenti)}")
    print()


    # ========================================================
    # CONTATORI
    # ========================================================

    migrati = 0
    gia_hashati = 0
    senza_password = 0


    # ========================================================
    # MIGRAZIONE PASSWORD
    # ========================================================

    for utente in utenti:

        user_id = utente["id_user"]
        email = utente["email"]
        password = utente["password"]


        # ----------------------------------------------------
        # PASSWORD ASSENTE
        # ----------------------------------------------------

        if not password:

            senza_password += 1

            print(f"[SALTATO] {email} - password assente")

            continue


        # ----------------------------------------------------
        # CONTROLLO PASSWORD GIÀ HASHATA
        # ----------------------------------------------------

        if password.startswith(
            ("$2a$", "$2b$", "$2y$")
        ):

            gia_hashati += 1

            print(f"[OK] {email} - password già hashata")

            continue


        # ----------------------------------------------------
        # CREAZIONE HASH BCRYPT
        # ----------------------------------------------------

        hashed_password = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")


        # ----------------------------------------------------
        # AGGIORNAMENTO DATABASE
        # ----------------------------------------------------

        cursor.execute("""
            UPDATE UTENTI
            SET password = %s
            WHERE id_user = %s
        """, (
            hashed_password,
            user_id
        ))


        migrati += 1

        print(f"[MIGRATA] {email}")


    # ========================================================
    # SALVATAGGIO MODIFICHE
    # ========================================================

    db.commit()


    # ========================================================
    # RIEPILOGO
    # ========================================================

    print()
    print("==============================================")
    print("          MIGRAZIONE COMPLETATA")
    print("==============================================")
    print(f"Utenti totali:        {len(utenti)}")
    print(f"Password migrate:     {migrati}")
    print(f"Già hashate:          {gia_hashati}")
    print(f"Senza password:       {senza_password}")
    print("==============================================")


except Exception as e:

    print()
    print("==============================================")
    print("       ERRORE DURANTE LA MIGRAZIONE")
    print("==============================================")
    print(f"Errore: {e}")
    print("==============================================")

    # Annulla eventuali modifiche se si verifica un errore
    if db:
        db.rollback()


finally:

    # Chiude il cursore
    if cursor:
        cursor.close()

    # Chiude la connessione
    if db:
        db.close()

    print()
    print("Connessione al database chiusa.")
