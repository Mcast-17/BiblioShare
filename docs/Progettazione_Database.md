## Progettazione della base di dati - BiblioShare
# Introduzione

La progettazione della base di dati rappresenta una fase fondamentale nello sviluppo del sistema BiblioShare, in quanto permette di definire in maniera strutturata l'organizzazione delle informazioni gestite dall'applicazione.
Il database ha il compito di memorizzare e gestire tutte le informazioni relative agli utenti registrati, ai libri condivisi sulla piattaforma e alle richieste di prestito effettuate tra gli utenti.
La progettazione è stata realizzata seguendo un approccio progressivo, partendo dalla definizione del modello concettuale tramite diagramma Entity-Relationship (EER), 
per poi arrivare alla traduzione nel modello relazionale successivamente implementato 
attraverso MySQL.

## Modello concettuale EER
Il modello Entity-Relationship consente di rappresentare graficamente la struttura informativa del sistema, identificando le principali entità coinvolte e le relazioni che intercorrono tra esse.
Il diagramma EER di BiblioShare individua principalmente le seguenti entità:

## UTENTI
Rappresenta gli utenti registrati alla piattaforma.
Gli attributi principali sono:
1. identificativo utente
2. nome
3. cognome
4. email
5. password
6. città
7. coordinate geografiche
L'entità permette di associare ogni utente ai libri pubblicati e alle richieste di prestito effettuate.

## LIBRI
Rappresenta il patrimonio librario condiviso dagli utenti.
Gli attributi principali sono:
1. identificativo libro
2. titolo
3. autore
4. categoria
5. anno di pubblicazione
6. descrizione
7. disponibilità
8. numero visualizzazioni
Ogni libro appartiene ad un determinato utente proprietario.

## RICHIESTA_PRESTITO

Rappresenta le richieste di prestito generate dagli utenti interessati ai libri disponibili sulla piattaforma.
Gli attributi principali sono:
1. identificativo richiesta
2. stato della richiesta
3. utente richiedente
4. libro richiesto
Questa entità permette di gestire il flusso delle richieste tra proprietari e utenti interessati.

##Schema relazionale

Dal modello concettuale è stato successivamente derivato lo schema relazionale implementato nel database MySQL.

La struttura logica del database comprende le seguenti relazioni principali:

UTENTI(id_user, nome, cognome, email, password, citta, latitudine, longitudine)
- Chiave primaria: id_user

LIBRI(id_libro, id_utente, titolo, autore, categoria, anno, descrizione, disponibilita, numero_visualizzazioni)
- Chiave primaria: id_libro
- Chiave esterna: id_utente → UTENTI(id_user) (rappresenta la proprietà del libro)

RICHIESTA_PRESTITO(id_richiesta, id_libro, id_richiedente, stato)
- Chiave primaria: id_richiesta
- Chiavi esterne: 
  - id_libro → LIBRI(id_libro)
  - id_richiedente → UTENTI(id_user) (utente che effettua la richiesta)



## Implementazione nel database MySQL

Il modello progettato è stato implementato tramite un database relazionale MySQL denominato:biblioteca_share
Il database contiene le tabelle necessarie al funzionamento dell'applicazione Flask e garantisce:
integrità dei dati;
collegamenti tramite chiavi primarie e straniere;
eliminazione delle ridondanze;
gestione efficiente delle interrogazioni.
Le operazioni effettuate dal backend Flask vengono eseguite tramite PyMySQL utilizzando query parametrizzate, migliorando sicurezza e affidabilità del sistema.

## Considerazioni finali
La progettazione della base di dati ha consentito di ottenere una struttura organizzata, scalabile e coerente con gli obiettivi del progetto BiblioShare.
La separazione tra modello concettuale, schema relazionale e implementazione fisica permette una migliore comprensione dell'architettura dati e 
garantisce una base solida per lo sviluppo delle funzionalità applicative, 
come autenticazione utenti, gestione dei libri, richieste di prestito e servizi di ricerca geografica.
