-- Richieste di prestito con utente e libro --
SELECT
    R.id_richiesta,
    U.nome,
    U.cognome,
    L.titolo,
    R.data_richiesta,
    R.stato
FROM RICHIESTA_PRESTITO R
JOIN UTENTI U
ON R.id_richiedente = U.id_user
JOIN LIBRI L
ON R.id_libro = L.id_libro;