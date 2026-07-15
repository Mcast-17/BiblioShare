-- Visualizzazione libri con il proprietario--
SELECT
    L.titolo,
    L.autore,
    L.categoria,
    U.nome,
    U.cognome,
    U.citta
FROM LIBRI L
JOIN UTENTI U
ON L.id_utente = U.id_user;