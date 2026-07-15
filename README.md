## 📚BiblioShare

## Descrizione del progetto
BiblioShare è una piattaforma web sviluppata in Python utilizzando il framework Flask, progettata per consentire agli utenti di condividere il proprio patrimonio librario e gestire richieste di prestito tra privati.
## Obiettivo del progetto 
L'obiettivo del progetto è favorire la condivisione della cultura attraverso una piattaforma semplice, intuitiva e sicura, integrando funzionalità di autenticazione, gestione del catalogo personale, ricerca dei libri, geolocalizzazione e visualizzazione cartografica mediante OpenStreetMap e Leaflet.js.

---

## Tecnologie utilizzate

- Backend: Python 3, Flask
- Database: MySQL, PyMySQL
- Autenticazione & Sicurezza: bcrypt, python-dotenv
- Frontend: HTML5, CSS3, Bootstrap 5, JavaScript
- Data Visualization: Chart.js
- Mappe & Geolocalizzazione: OpenStreetMap, Leaflet.js

---

## Funzionalità implementate

### Gestione utenti
- Registrazione utenti
- Login sicuro con gestione delle sessioni Flask
- Logout sicuro con distruzione della sessione
- Modifica del profilo utente

### Gestione libri
- Inserimento, modifica ed eliminazione del libro (CRUD completo)
- Visualizzazione dei propri libri in un catalogo dedicato
- Ricerca testuale avanzata dei volumi disponibili

### Geolocalizzazione
- Visualizzazione dinamica dei libri sulla mappa
- Ricerca geospaziale avanzata dei volumi vicini
- Calcolo delle distanze reali tramite la formula di Haversine
- Integrazione nativa con OpenStreetMap e Leaflet.js

### Dashboard
- Statistiche generali degli utenti della piattaforma
- Grafico interattivo dei libri più visualizzati
- Conteggio e storico dei prestiti effettuati
- Pannello di navigazione rapida

### API REST
Il backend espone diversi endpoint JSON per l'interazione disaccoppiata:
- Elenco completo dei libri
- Conteggio utenti totali
- Statistiche dei prestiti
- Libri attualmente disponibili
- Top libri più popolari
- Ricerca filtrata per categoria
- Tracciamento dei dati geografici

---

## Sicurezza

In conformità con le linee guida per lo sviluppo sicuro del software e la gestione delle credenziali sensibili, il sistema implementa le seguenti misure di protezione:
- Gestione Credenziali Segrete: La chiave segreta di Flask (SECRET_KEY) e le credenziali di accesso al database MySQL (DB_PASSWORD) sono state rimosse dal codice sorgente e vengono caricate a runtime tramite variabili d'ambiente protette (file .env escluso dal tracciamento Git).
- Cifratura Password: Password degli utenti salvate nel database esclusivamente tramite hash crittografico sicuro grazie a bcrypt.
- Query Parametrizzate: Interazioni con il database MySQL protette nativamente contro attacchi di tipo SQL Injection.
- Protezione Aree Riservate: Controllo degli accessi e delle sessioni per impedire la navigazione non autorizzata nelle pagine private del backend.

---

## Installazione e Configurazione
1. **Clonare il repository:**  https://github.com/Mcast-17/BiblioShare.git
2. **Installare le dipendenze necessarie:**   pip install -r app/requirements.txt
3. **Crea un file chiamato esattamente .env all'interno della cartella app/ e inserisci i tuoi parametri locali seguendo questa struttura:**                    SECRET_KEY=la_tua_chiave_segreta_qui

     DB_HOST=localhost
     
     DB_USER=il_tuo_utente_mysql
     
     DB_PASSWORD=la_tua_password_mysql
     
     DB_NAME=biblioteca_share

5. **Creare il database MySQL ed importare biblioteca_share.sql:**
Importa il file SQL nel tuo gestore di database locale per generare lo schema e le tabelle.
6. **Avviare il server Flask:**    
    python app.py
7. **Aprire il browser:**
   Naviga all'indirizzo [http://127.0.0.1:5000](http://127.0.0.1:5000) per utilizzare l'applicazione.

---

##Database

Il progetto utilizza un database MySQL denominato biblioteca_share.

Il file biblioteca_share.sql contiene l'intera struttura del database, comprensiva di:
tabelle
chiavi primarie
chiavi esterne
relazioni
dati iniziali

Sono inoltre presenti alcuni script SQL utilizzati per testare interrogazioni e funzionalità del sistema:

Ordinamento dei libri in base al numero di visualizzazioni
Ricerca libri per categoria
Richieste di prestito con utente e libro
Visualizzazione degli utenti
Visualizzazione dei libri con il proprietario
Visualizzazione dei libri disponibili
Visualizzazione delle richieste di prestito

##Gestione delle copertine

Per evitare problematiche legate al copyright delle copertine dei libri commerciali, il sistema utilizza una copertina generica denominata:default_book.jpg
Questa immagine viene utilizzata come copertina predefinita del progetto, garantendo uniformità grafica e assenza di violazioni dei diritti d'autore.

---

## Struttura del progetto
<pre><code>BiblioShare/
│
├── migrate_passwords.py              # Script per la migrazione delle password
│
├── venv/                             # Ambiente virtuale Python (da escludere da Git)
│
├── static/                           # File statici principali
│   ├── style.css                     # CSS globale
│   ├── JS/                           # Script JavaScript esterni
│   ├── CSS/                          # File CSS aggiuntivi
│   └── covers/                       # Copertine libri
│
├── app/                              # Applicazione Flask
│   ├── app.py                        # File principale Flask
│   ├── requirements.txt              # Dipendenze Python
│   ├── .env                          # Variabili ambiente locali (segrete)
│   ├── .gitignore                    # Esclusione file sensibili
│   ├── README.md                     # Documentazione applicazione
│   │
│   ├── templates/                    # File HTML frontend
│   │   ├── index.html
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── dashboard.html
│   │   ├── profile.html
│   │   ├── my_books.html
│   │   ├── add_book.html
│   │   ├── edit_book.html
│   │   ├── search.html
│   │   ├── geo_search.html
│   │   └── map.html
│   │
│   ├── biblioteca_share/             # File relativi al database
│   │   ├── biblioteca_share.sql
│   │   ├── Ordinamento dei libri in base al numero di visualizzazioni.sql
│   │   ├── Ricerca libri per categorie.sql
│   │   ├── Richieste di prestito con utente e libro.sql
│   │   ├── Visualizzazione degli utenti.sql
│   │   ├── Visualizzazione libri con il proprietario.sql
│   │   ├── Visualizzazione libri per disponibilità.sql
│   │   └── Visualizzazione richieste di prestito.sql
│   │
│   └── static/                       # File statici interni Flask
│       └── covers/                   # Copertine caricate dagli utenti
│
├── docs/                             # Documentazione progetto
│   ├── README.md
│   ├── Diagramma_EER.png
│   └── Schema_Relazionale.png
│
└── immagini/                         # Screenshot applicazione
    ├── homepage.png
    ├── dashboard.png
    ├── mappa.png
    ├── libriUtente.png
    ├── profilo.png
    └── statistiche.png</code></pre>

---

## Autore

- Sviluppatore: Mattia Castiello 
- Anno Accademico: 2025/2026
- Università: Università Telematica Pegaso

---

## Licenza

Il presente progetto è stato sviluppato esclusivamente per elaborato tesi di laurea 
