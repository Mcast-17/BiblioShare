-- Ricerca libri per categorie--
-- Utilizzo della clausola IN per filtrare più categorie in modo compatto e leggibile,evitando 
-- l'uso di più condizioni OR e rendendo la query più semplice da mantenere.
SELECT *
FROM LIBRI
WHERE categoria IN ('fantascienza', 'storico', 'Distopico','Filosofico','fantasy','romantico','saggistica');
