# Import Flask e strumenti principali per routing, sessioni, template e API JSON
from flask import Flask, render_template, jsonify, request, redirect, url_for, session, flash,current_app

# Libreria per connessione MySQL
import pymysql  # per la connessione con MYSQL

# Libreria per hashing password (sicurezza)
import bcrypt  # per le password hash

# Utility per creare decoratori (es. login_required)
from functools import wraps  # per il decoratore

# Libreria matematica (usata per distanza geografica Haversine)
import math  # Per la funzione Haversine

import os#Interazione con il sistema operativo
import uuid#Utilizzata come interazione per generazione di identificativi univici 

from dotenv import load_dotenv  #Libreria esterna per caricare le variabili segrete dal file .env


#Carica il file .env presente nella stessa cartella dello script
load_dotenv()

# Creazione dell'istanza Flask per avviare l'applicazione web
app = Flask(__name__)

# Configurazione della chiave segreta per gestire le sessioni e i cookie in sicurezza.
# os.getenv("SECRET_KEY") va a leggere il valore nascosto dentro al file .env.
# Se qualcuno scarica il codice da GitHub senza il file .env, la tua chiave reale rimane segreta.
app.secret_key = os.getenv("SECRET_KEY")



# ---------------------------
# CONNESSIONE DATABASE
# ---------------------------
def get_db_connection():
    """
    Crea e restituisce una connessione al database MySQL.
    Utilizza cursor DictCursor per ottenere risultati come dizionari.
    """
    return pymysql.connect(
        host="localhost",
        user="root",
        password=os.getenv("DB_PASSWORD"),#Recupera la password dal file .env
        database="biblioteca_share",
        cursorclass=pymysql.cursors.DictCursor
    )


# ---------------------------
# DECORATORE: LOGIN OBBLIGATORIO
# ---------------------------
def login_required(f):
    """
    Decoratore che blocca l'accesso alle route se l'utente non è loggato.
    Controlla la presenza di 'user_id' nella sessione.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function


# ---------------------------
# HOMEPAGE
# ---------------------------
@app.route("/")
def home():
    """Pagina iniziale del sito"""
    return render_template("index.html")


# ---------------------------
# REGISTRAZIONE UTENTE
# ---------------------------
@app.route("/register", methods=["GET", "POST"])
def register():

    # Se form inviato
    if request.method == "POST":

        # Recupero dati dal form
        nome = request.form["nome"]
        cognome = request.form["cognome"]
        email = request.form["email"]
        password = request.form["password"]
        citta = request.form["citta"]

        # Connessione DB
        db = get_db_connection()
        cursor = db.cursor()

        # Controllo se email già esiste
        cursor.execute("SELECT * FROM UTENTI WHERE email=%s", (email,))
        if cursor.fetchone():
            flash("Email già registrata.")
            cursor.close()
            db.close()
            return redirect(url_for("register"))

        # Hash della password (sicurezza)
        password_hash = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

        # Inserimento nuovo utente
        cursor.execute("""
            INSERT INTO UTENTI (nome, cognome, email, password, citta)
            VALUES (%s, %s, %s, %s, %s)
        """, (nome, cognome, email, password_hash, citta))

        db.commit()
        cursor.close()
        db.close()

        flash("Registrazione completata!")
        return redirect(url_for("login"))

    # GET request → mostra pagina registrazione
    return render_template("register.html")


# ---------------------------
# LOGIN UTENTE
# ---------------------------
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        # Dati login
        email = request.form.get("email")
        password = request.form.get("password")

        # Connessione DB
        db = get_db_connection()
        cursor = db.cursor()

        # Cerca utente
        cursor.execute("SELECT * FROM UTENTI WHERE email=%s", (email,))
        user = cursor.fetchone()

        cursor.close()
        db.close()

        # Verifica password hash
        if user and bcrypt.checkpw(
            password.encode("utf-8"),
            user["password"].encode("utf-8")
        ):
            # Salvataggio sessione
            session["user_id"] = user["id_user"]
            session["nome"] = user["nome"]

            return redirect(url_for("dashboard"))

        return render_template("login.html", errore="Email o password errati.")

    return render_template("login.html")


# ---------------------------
# LOGOUT UTENTE
# ---------------------------
@app.route("/logout")
def logout():
    """Svuota la sessione utente"""
    session.clear()
    return redirect(url_for("home"))


# ----------------------------------------
# DASHBOARD (ACCESSO PROTETTO)
# ----------------------------------------
@app.route("/dashboard")
@login_required
def dashboard():

    # ID utente loggato
    user_id = session.get('user_id')

    # Connessione DB
    db = get_db_connection()
    cursor = db.cursor()

    # Conteggio richieste prestito dell'utente
    cursor.execute("""
        SELECT COUNT(*) AS totale 
        FROM RICHIESTA_PRESTITO 
        WHERE id_richiedente = %s
    """, (user_id,))

    risultato = cursor.fetchone()

    # Gestione output variabile DB
    if isinstance(risultato, dict):
        prestiti_count = risultato['totale']
    elif isinstance(risultato, (tuple, list)) and len(risultato) > 0:
        prestiti_count = risultato[0]
    else:
        prestiti_count = 0

    cursor.close()
    db.close()

    # Render dashboard
    return render_template(
        "dashboard.html",
        nome=session.get("nome"),
        prestiti_utente=prestiti_count
    )


# ---------------------------
# API: CONTEGGIO UTENTI
# ---------------------------
@app.route("/api/utenti/count")
def count_utenti():

    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute("SELECT COUNT(*) AS totale_utenti FROM UTENTI")
    result = cursor.fetchone()

    db.close()
    return jsonify(result)


# ---------------------------
# PROFILO UTENTE
# ---------------------------
@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():

    db = get_db_connection()
    cursor = db.cursor()

    user_id = session["user_id"]

    # Aggiornamento profilo
    if request.method == "POST":

        nome = request.form["nome"]
        cognome = request.form["cognome"]
        citta = request.form["citta"]
        password = request.form["password"]

        # Se password cambiata
        if password != "":

            password_hash = bcrypt.hashpw(
                password.encode("utf-8"),
                bcrypt.gensalt()
            ).decode("utf-8")

            cursor.execute("""
                UPDATE UTENTI
                SET nome=%s,
                    cognome=%s,
                    citta=%s,
                    password=%s
                WHERE id_user=%s
            """,(nome,cognome,citta,password_hash,user_id))

        else:

            cursor.execute("""
                UPDATE UTENTI
                SET nome=%s,
                    cognome=%s,
                    citta=%s
                WHERE id_user=%s
            """,(nome,cognome,citta,user_id))

        db.commit()

        # aggiorna sessione
        session["nome"]=nome

        flash("Profilo aggiornato con successo!")

    # Recupero dati utente aggiornati
    cursor.execute("""
        SELECT *
        FROM UTENTI
        WHERE id_user=%s
    """,(user_id,))

    utente = cursor.fetchone()

    cursor.close()
    db.close()

    return render_template("profile.html",utente=utente)


# ---------------------------
# API: LIBRI
# ---------------------------
@app.route("/api/libri")
def libri():

    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute("""
        SELECT L.titolo, L.autore, L.categoria,
               U.nome, U.cognome, U.citta,
               U.latitudine, U.longitudine
        FROM LIBRI L
        JOIN UTENTI U ON L.id_utente = U.id_user
    """)

    result = cursor.fetchall()
    db.close()
    return jsonify(result)


# ---------------------------
# API: PRESTITI
# ---------------------------
@app.route("/api/prestiti")
def prestiti():

    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute("""
        SELECT R.id_richiesta, L.titolo,
               U.nome, U.cognome, R.stato
        FROM RICHIESTA_PRESTITO R
        JOIN LIBRI L ON R.id_libro = L.id_libro
        JOIN UTENTI U ON R.id_richiedente = U.id_user
    """)

    rows = cursor.fetchall()
    db.close()

    # Conversione manuale in JSON
    result = []
    for r in rows:
        result.append({
            "id_richiesta": r[0],
            "titolo": r[1],
            "nome": r[2],
            "cognome": r[3],
            "stato": r[4]
        })

    return jsonify(result)


# ---------------------------
# API: STATO RICHIESTE
# ---------------------------
@app.route("/api/richieste/stato")
def stato():

    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute("""
        SELECT stato, COUNT(*) as totale
        FROM RICHIESTA_PRESTITO
        GROUP BY stato
    """)

    rows = cursor.fetchall()
    db.close()

    result = []

    for r in rows:
        result.append({
            "stato": r["stato"],
            "totale": r["totale"]
        })

    return jsonify(result)


# ---------------------------
# API: TOP LIBRI
# ---------------------------
@app.route("/api/top_libri")
def top_libri():

    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute("""
        SELECT id_libro, titolo, autore, numero_visualizzazioni
        FROM LIBRI
        ORDER BY numero_visualizzazioni DESC
        LIMIT 4
    """)

    result = cursor.fetchall()
    db.close()
    return jsonify(result)


# ---------------------------
# API: LIBRI PER CATEGORIA
# ---------------------------
@app.route("/api/libri_categoria")
def libri_categoria():

    categoria = request.args.get("cat")

    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute("""
        SELECT *
        FROM LIBRI
        WHERE LOWER(categoria) = LOWER(%s)
    """, (categoria,))

    result = cursor.fetchall()
    db.close()
    return jsonify(result)


# ---------------------------
# API: LIBRI DISPONIBILI
# ---------------------------
@app.route("/api/libri_disponibili")
def libri_disponibili():

    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute("""
        SELECT *
        FROM LIBRI
        WHERE disponibilita = TRUE
    """)

    result = cursor.fetchall()
    db.close()
    return jsonify(result)


# ---------------------------
# API: LIBRI CON COORDINATE
# ---------------------------
@app.route("/api/libri_geo")
def libri_geo():

    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute("""
        SELECT L.*, U.latitudine, U.longitudine
        FROM LIBRI L
        JOIN UTENTI U ON L.id_utente = U.id_user
        WHERE U.latitudine IS NOT NULL
        AND U.longitudine IS NOT NULL
    """)

    result = cursor.fetchall()
    db.close()
    return jsonify(result)


# -------------------
# LIBRI DELL'UTENTE
# -------------------
@app.route('/my_books')
def my_books():

    if 'user_id' not in session:
        return redirect('/login')

    db = get_db_connection()
    cursor = db.cursor()

    # libri dell'utente loggato
    cursor.execute("""
        SELECT * FROM libri
        WHERE id_utente = %s
    """, (session['user_id'],))
    libri = cursor.fetchall()

    # conteggio prestiti utente
    cursor.execute("""
        SELECT COUNT(*) AS totale 
        FROM RICHIESTA_PRESTITO 
        WHERE id_richiedente = %s
    """, (session['user_id'],))

    risultato = cursor.fetchone()

    if isinstance(risultato, dict):
        prestiti_count = risultato['totale']
    elif isinstance(risultato, (tuple, list)):
        prestiti_count = risultato[0]
    else:
        prestiti_count = 0

    cursor.close()
    db.close()

    return render_template("my_books.html", libri=libri, prestiti_utente=prestiti_count)


# -------------------
# AGGIUNGI LIBRO
# -------------------
@app.route("/add_book", methods=["GET", "POST"])
def add_book():

    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":

        titolo = request.form.get("titolo")
        autore = request.form.get("autore")
        categoria = request.form.get("categoria")
        anno = request.form.get("anno")
        descrizione = request.form.get("descrizione")
        
        #Gestione e salvataggio dell'immagine di copertina#
        file = request.files.get("copertina")
        
        upload_folder = os.path.join(current_app.root_path, "static", "covers")
        os.makedirs(upload_folder, exist_ok=True)

        if file and file.filename != "":
            filename = file.filename
            save_path = os.path.join(upload_folder, filename)
            file.save(save_path)
        else:
            filename = "default_book.jpg"

        # GESTIONE FILE
        if file and file.filename != "":
            ext = os.path.splitext(file.filename)[1]  # .jpg, .png ecc
            filename = f"{uuid.uuid4().hex}{ext}"     # nome unico

            save_path = os.path.join(upload_folder, filename)
            file.save(save_path)

        else:
            filename = "default_book.jpg"

        # SALVATAGGIO DB (SOLO NOME FILE)
        db = get_db_connection()
        cursor = db.cursor()

        cursor.execute("""
            INSERT INTO LIBRI
            (id_utente, titolo, autore, categoria, anno, descrizione, disponibilita, numero_visualizzazioni, copertina)
            VALUES (%s,%s,%s,%s,%s,%s,1,0,%s)
        """, (
            session["user_id"],
            titolo,
            autore,
            categoria,
            anno,
            descrizione,
            filename
        ))

        db.commit()
        cursor.close()
        db.close()

        return redirect("/my_books")

    return render_template("add_book.html")


# -------------------
# MODIFICA LIBRO
# -------------------
@app.route("/edit_book/<int:id>", methods=["GET", "POST"])
def edit_book(id):

    if "user_id" not in session:
        return redirect("/login")

    db = get_db_connection()
    cursor = db.cursor()

    # recupero libro dell'utente
    cursor.execute("""
        SELECT * FROM LIBRI
        WHERE id_libro=%s AND id_utente=%s
    """, (id, session["user_id"]))

    libro = cursor.fetchone()

    if request.method == "POST":

        titolo = request.form["titolo"]
        autore = request.form["autore"]
        categoria = request.form["categoria"]
        anno = request.form["anno"]
        descrizione = request.form["descrizione"]

        cursor.execute("""
            UPDATE LIBRI
            SET titolo=%s,
                autore=%s,
                categoria=%s,
                anno=%s,
                descrizione=%s
            WHERE id_libro=%s AND id_utente=%s
        """, (
            titolo, autore, categoria, anno, descrizione,
            id, session["user_id"]
        ))

        db.commit()
        cursor.close()
        db.close()

        return redirect("/my_books")

    cursor.close()
    db.close()

    return render_template("edit_book.html", libro=libro)


# -------------------
# ELIMINA LIBRO
# -------------------
@app.route("/delete_book/<int:id>")
def delete_book(id):

    if "user_id" not in session:
        return redirect("/login")

    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute("""
        DELETE FROM LIBRI
        WHERE id_libro=%s AND id_utente=%s
    """, (id, session["user_id"]))

    db.commit()

    cursor.close()
    db.close()

    return redirect("/my_books")


# -----------------------------
# RICERCA LIBRI
# -----------------------------
@app.route("/search", methods=["GET"])
@login_required
def search():

    testo = request.args.get("q", "")

    db = get_db_connection()
    cursor = db.cursor()

    if testo == "":

        cursor.execute("""
            SELECT
                L.id_libro,
                L.titolo,
                L.autore,
                L.categoria,
                L.anno,
                L.disponibilita,
                U.nome,
                U.cognome,
                U.citta
            FROM LIBRI L
            JOIN UTENTI U
            ON L.id_utente = U.id_user
            ORDER BY titolo
        """)

    else:

        ricerca = "%" + testo + "%"

        cursor.execute("""
            SELECT
                L.id_libro,
                L.titolo,
                L.autore,
                L.categoria,
                L.anno,
                L.disponibilita,
                U.nome,
                U.cognome,
                U.citta
            FROM LIBRI L
            JOIN UTENTI U
            ON L.id_utente = U.id_user

            WHERE
                L.titolo LIKE %s
                OR L.autore LIKE %s
                OR L.categoria LIKE %s

            ORDER BY titolo
        """,(ricerca,ricerca,ricerca))

    libri = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template(
        "search.html",
        libri=libri,
        ricerca=testo
    )


# ------------------
# FUNZIONE HAVERSINE
# ------------------
def haversine(lat1, lon1, lat2, lon2):

    # raggio terrestre in km
    R = 6371

    # differenze in radianti
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    # formula Haversine
    a = math.sin(dlat/2)**2 + \
        math.cos(math.radians(lat1)) * \
        math.cos(math.radians(lat2)) * \
        math.sin(dlon/2)**2

    c = 2 * math.asin(math.sqrt(a))

    return R * c


# ---------------------------
# API: RICERCA GEO
# ---------------------------
@app.route("/api/search_geo")
@login_required
def api_search_geo():

    try:
        lat = float(request.args.get("lat"))
        lon = float(request.args.get("lon"))
        radius = float(request.args.get("radius"))
    except (TypeError, ValueError):
        return jsonify({"errore": "Parametri non validi"}), 400

    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute("""
        SELECT
            L.id_libro,
            L.titolo,
            L.autore,
            L.categoria,
            U.nome,
            U.cognome,
            U.citta,
            U.latitudine,
            U.longitudine
        FROM LIBRI L
        JOIN UTENTI U
            ON L.id_utente = U.id_user
        WHERE
            U.latitudine IS NOT NULL
            AND U.longitudine IS NOT NULL
    """)

    libri = cursor.fetchall()

    risultati = []

    # filtro per distanza geografica
    for libro in libri:

        distanza = haversine(
            lat,
            lon,
            float(libro["latitudine"]),
            float(libro["longitudine"])
        )

        if distanza <= radius:

            risultati.append({
                "id_libro": libro["id_libro"],
                "titolo": libro["titolo"],
                "autore": libro["autore"],
                "categoria": libro["categoria"],
                "nome": libro["nome"],
                "cognome": libro["cognome"],
                "citta": libro["citta"],
                "latitudine": libro["latitudine"],
                "longitudine": libro["longitudine"],
                "distanza_km": round(distanza, 2)
            })

    cursor.close()
    db.close()

    # ordinamento per distanza
    risultati.sort(key=lambda x: x["distanza_km"])

    return jsonify(risultati)


# -------------------
# API: MAPPA LIBRI
# -------------------
@app.route("/api/map_libri") 
def map_libri(): 
    db = get_db_connection() 
    cursor = db.cursor() 
    
    cursor.execute(""" 
       SELECT 
        L.titolo, 
        L.autore, 
        U.nome, 
        U.cognome, 
        U.latitudine, 
        U.longitudine 
       FROM LIBRI L 
       JOIN UTENTI U ON L.id_utente = U.id_user 
       WHERE U.latitudine IS NOT NULL 
       AND U.longitudine IS NOT NULL 
    """) 
    
    result = cursor.fetchall() 
    
    cursor.close() 
    db.close() 
    
    return jsonify(result)


# -------------------
# PAGINA RICERCA GEO
# -------------------
@app.route("/geo_search")
@login_required
def geo_search():
    return render_template("geo_search.html")


# -------------------
# PAGINA MAPPA
# -------------------
@app.route("/mappa")
def mappa():

    if "user_id" not in session:
        return redirect("/login")

    return render_template("map.html")


# ---------------------------
# AVVIO APP FLASK
# ---------------------------
if __name__ == "__main__":
    app.run(debug=True)