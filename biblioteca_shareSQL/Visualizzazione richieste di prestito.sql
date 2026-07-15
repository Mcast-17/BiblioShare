-- Visualizzazione richieste di prestito -- 
SELECT R.id_richiesta, L.titolo, U.nome, R.stato
FROM RICHIESTA_PRESTITO R
JOIN LIBRI L ON R.id_libro = L.id_libro
JOIN UTENTI U ON R.id_richiedente = U.id_user;