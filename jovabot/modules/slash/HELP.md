I messaggi a cui rispondera' il buon jova dovranno sempre contenere `jova` nella frase, fatta eccezione per i comandi speciali `/help` e `/about`.

In breve i comandi principali che potete impartire al bot:

1. `Jova se ti dico CONDIZIONE tu rispondi RISPOSTA_ALLA_CONDIZIONE`:
    1. Salvera' su un database la condizione e la riposta a tale condizione (le risposte possono essere multiple)
    2. La risposta non verra' salvata se la condizione e' gia presente tra quelle di `Jova a cosa rispondi`

2. `Jova cercami ROBA a NOME_CITTA`:
    1. Effettua una ricerca sulle pagine bianche (http://www.paginebianche.it/)

3. `Jova l'oroscopo per SEGNI_O_SEGNO`:
    1. Esempio: `Jova l'oroscopo per sagittario vergine cancro`, risponde con l'oroscopo giornaliero per i segni elencati
    2. Preso dal sito http://it.horoscopofree.com

4. `Jova CONDIZIONE`:
    1. Risponde con un messaggio dal file delle risposte per quella data condizione, vedere `Jova a cosa rispondi` per maggiori dettagli, per ogni condizione c'e' una lista di possibili risposte, che verranno scelte casualmente.
    2. Esempio: Scrivendo `jova una perla` otterrete una risposta del genere: `L'occafione fa l'uomo ladro.`
    3. `Jova a cosa rispondi`
      1. Risponde con tutte le condizioni possibili ( per il punto 4 ).

5. `Jova PEZZO_DI_UNA_CANZONE` (se la condizione non e' stata soddisfatta da `jova CONDIZIONE`):
    1. Esempio: `jova serenata rap` ritorna il link a `shazam` per poter ascoltare la canzone
