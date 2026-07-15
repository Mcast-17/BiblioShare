-- Ordinamento dei libri in base al numero di visualizzazioni,
-- in modo decrescente, per ottenere i libri più popolari.
-- LIMIT 10 restituisce solo i primi 10 risultati.
SELECT *
FROM LIBRI
ORDER BY numero_visualizzazioni DESC
LIMIT 10;