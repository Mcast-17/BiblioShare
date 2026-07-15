-- Creazione database --
CREATE DATABASE biblioteca_share;
USE biblioteca_share;

-- Creazione tabella utenti --
CREATE TABLE UTENTI(

    id_user INT AUTO_INCREMENT PRIMARY KEY,

    nome VARCHAR(50) NOT NULL,

    cognome VARCHAR(50) NOT NULL,

    email VARCHAR(100) NOT NULL UNIQUE,

    password VARCHAR(255) NOT NULL,

    citta VARCHAR(50),

    latitudine FLOAT,

    longitudine FLOAT

);
-- Creazione tabella libri --
CREATE TABLE LIBRI(

    id_libro INT AUTO_INCREMENT PRIMARY KEY,

    id_utente INT NOT NULL,

    titolo VARCHAR(100) NOT NULL,

    autore VARCHAR(100) NOT NULL,

    isbn VARCHAR(20),

    anno INT,

    categoria VARCHAR(50),

    descrizione TEXT,

    copertina VARCHAR(255),

    disponibilita BOOLEAN DEFAULT TRUE,

    numero_visualizzazioni INT DEFAULT 0,

    data_inserimento DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (id_utente)
        REFERENCES UTENTI(id_user)

);

-- Creazione tabella richiesta_prestito -- 
CREATE TABLE RICHIESTA_PRESTITO(

    id_richiesta INT AUTO_INCREMENT PRIMARY KEY,

    id_libro INT NOT NULL,

    id_richiedente INT NOT NULL,

    data_richiesta DATE,

    stato VARCHAR(20),

    FOREIGN KEY (id_libro)
        REFERENCES LIBRI(id_libro),

    FOREIGN KEY (id_richiedente)
        REFERENCES UTENTI(id_user)

);
-- popolamento database --
INSERT INTO UTENTI (nome,cognome,email,password,citta,latitudine,longitudine)
VALUES
('Mario','Rossi','mario.Rossi@gmail.com','utenteRossi_13','Milano',45.4642,9.1900),
('Giulia','Bianchi','giulia.Bianchi@gmail.com','Gulybianchi','Roma',41.9028,12.4964),
('Sara','Ferrari','sara.Ferrari@gmail.com','PassFerrari123','Torino',45.0703,7.6869),
('Vittorio','Perna','vittPerna54@gmail.com','VPern54','Napoli',40.8518,14.2681);

INSERT INTO LIBRI 
(id_libro, id_utente, titolo, autore, isbn, anno, categoria, descrizione, copertina, disponibilita, numero_visualizzazioni)
VALUES
(1, 1, 'Il Nome della Rosa', 'Umberto Eco', '9780156001311', 1980, 'Storico', 'Romanzo ambientato in un monastero medievale', 'nome_rosa.jpg', TRUE, 5),
(2, 1, 'Dune', 'Frank Herbert', '9780441172719', 1965, 'Fantascienza', 'Capolavoro della fantascienza', 'dune.jpg', TRUE, 12),
(3, 2, '1984', 'George Orwell', '9780451524935', 1949, 'Distopico', 'Società controllata dal Grande Fratello', '1984.jpg', TRUE, 20),
(4, 2, 'Il Piccolo Principe', 'Antoine de Saint-Exupéry', '9780156012195', 1943, 'Filosofico', 'Favola poetica', 'principe.jpg', TRUE, 18),
(5, 3, 'Harry Potter e la Pietra Filosofale', 'J.K. Rowling', '9780747532743', 1997, 'Fantasy', 'Inizio saga di Harry Potter', 'hp1.jpg', TRUE, 30),
(6, 3, 'Il Signore degli Anelli', 'J.R.R. Tolkien', '9780618640157', 1954, 'Fantasy', 'Epica avventura nella Terra di Mezzo', 'lotr.jpg', TRUE, 25),
(7, 4, 'Orgoglio e Pregiudizio', 'Jane Austen', '9780141439518', 1813, 'Romantico', 'Romanzo classico inglese', 'austen.jpg', TRUE, 10),
(8, 4, 'Sapiens', 'Yuval Noah Harari', '9780062316097', 2011, 'Saggistica', 'Storia dell’umanità', 'sapiens.jpg', TRUE, 15);

INSERT INTO RICHIESTA_PRESTITO
(id_libro, id_richiedente, data_richiesta, stato)
VALUES
(1, 2, CURDATE(), 'In attesa'),
(2, 1, CURDATE(), 'Accettata'),
(3, 4, CURDATE(), 'Rifiutata'),
(4, 3, CURDATE(), 'In attesa');