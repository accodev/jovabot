# [Jovanotti](https://it.wikipedia.org/wiki/Jovanotti) bot per telegram

![ti tiro un faffo!](http://i.imgur.com/DHlVkqo.jpg)

[![Build Status](https://travis-ci.org/Shevraar/jovabot.svg?branch=develop)](https://travis-ci.org/Shevraar/jovabot) [![Code Climate](https://codeclimate.com/github/Shevraar/jovabot/badges/gpa.svg)](https://codeclimate.com/github/Shevraar/jovabot)

### Come aggiungerlo su telegram

Aggiungere ad un gruppo o mandare un messaggio direttamente a **@jovanottibot**


### Introduzione

Questo bot rimpiazza tutte le 's' (e quando gli va', anche le 'z') con 'f' in tutte le risposte che da...

La privacy non e' abilitata per questo bot, quindi ogni volta che il bot ricevera' un messaggio, verra' letto. E' stato implementato in questo modo per farlo comportare come una persona vera che risponde ai messaggi.

### Come invocare il jova

I messaggi a cui rispondera' saranno sempre messaggi che contengano jova nella frase, in breve i comandi principali che potete dare al bot:

1. *Jova se ti dico ```CONDIZIONE``` tu rispondi ```RISPOSTA_ALLA_CONDIZIONE```*:
    1. Questo salvera' su un database la condizione e la riposta alla condizione (le risposte possono essere multiple)


2. *Jova cercami ```ROBA``` a ```NOME_CITTA```*:
    1. Questo effettua una ricerca su pagine bianche e schiaffa l'output sulla chat

3. *Jova l'oroscopo per ```SEGNI\SEGNO```*:
    1. Esempio: Jova l'oroscopo per sagittario vergine cancro, risponde con l'oroscopo giornaliero

4. *Jova ```CONDIZIONE```*:
    1. Risponde con un messaggio dal file delle risposte per quella data condizione, vedere Jova help per maggiori dettagli, per ogni condizione c'e' una lista di possibili risposte, che verranno scelte casualmente.
    2. Esempio: jova una perla - otterrete una risposta del genere: "L'occafione fa l'uomo ladro."

5. *Jova help*
    1. Risponde con tutte le condizioni (per il punto 4) a cui puo' rispondere jova.

6. *Jova ```PEZZO_DI_UNA_CANZONE```* (se la condizione non e' stata soddisfatta da jova CONDIZIONE):
    1. Esempio: jova serenata rap ritorna il link a shazam per poter ascoltare la canzone
    2. Per ora sono poche le canzoni disponibili.

