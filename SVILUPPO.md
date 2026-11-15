# Nasone — note di sviluppo

Diario del progetto: decisioni prese, verifiche, domande aperte. Si aggiorna a ogni passo.

## Obiettivo

Web app installabile (PWA, anche su Google Play come app impacchettata) che trova il **nasone** più vicino,
la fontanella romana in ghisa, e disegna il percorso a piedi. Ha una pagina di storia e curiosità.
È la sorella di [Turet](https://github.com/pippotorre/turet): stesso motore, altra città e altra grafica.
Indirizzo: **https://nasone.entratadisicurezza.com/** (GitHub Pages, dominio personalizzato).

## Decisioni prese

| Data | Decisione |
|---|---|
| 26/10/2026 | Nata dal codice di Turet: sito statico, dati OpenStreetMap (Overpass + routing.openstreetmap.de), Leaflet in `vendor/`. |
| 26/10/2026 | Cinque lingue (IT, EN, FR, ES, DE), grafica porpora, ghisa e travertino, pagina `storia.html`. |
| 26/10/2026 | Illustrazione: solo la colonnina verde con pomello dorato, senza targa viola. |
| 26/10/2026 | Pubblicazione su Google Play come PWA impacchettata: guida in `docs/ANDROID.md`. |
| 26/10/2026 | Fino a 40 punti sulla mappa, inclusi i rubinetti potabili; link per segnalare fontanelle mancanti su OpenStreetMap. |
| 27/10/2026 | **Statistiche di visita con GoatCounter** (senza cookie, nessun dato personale): vedi sotto. |

## Statistiche (GoatCounter)

- Account unico per tutto il dominio: https://entratadisicurezza.goatcounter.com. Le app si distinguono dal percorso (`/nasone/`).
- Script in `index.html` e `storia.html`, prima di `</head>`; `privacy.html` non è contata.
  Il percorso inviato è `location.pathname` senza `index.html`.
- Eventi sul pulsante «Installa l'app» (`js/app.js`, funzione `conta`): `nasone-installa-clic`,
  `nasone-installa-rifiutata`, `nasone-installata` (quest'ultimo anche se si installa dal menu di Chrome).
  Su iPhone il pulsante è solo un'istruzione, quindi niente eventi.
- Nessun cookie, niente salvato nel browser, IP non conservato: non serve il banner.
- Limiti: chi usa un blocco pubblicità non viene contato; offline non si conta nulla.
- Informativa privacy aggiornata nelle 5 lingue e indicazioni per la «Sicurezza dei dati» in `docs/ANDROID.md`.
- Versione dei file portata a `?v=5` / `nasone-v5`.

## Verifiche fatte

- 27/10/2026 – Prova in Chromium simulando Android con lo script di GoatCounter vero: visite per `/nasone/` e
  `/nasone/storia.html`, nessuna per `privacy.html`, i tre eventi di installazione inviati. Nessun errore JavaScript.
  Test esistenti superati.

## Punti aperti

- [ ] Aggiornare il modulo «Sicurezza dei dati» nella Play Console.
- [ ] Dopo qualche giorno, controllare su GoatCounter che arrivino visite ed eventi.

| 14/11/2026 | Spostamento su GitHub Pages (nasone.entratadisicurezza.com). Dati a tessere (`data/t/`) rigenerati ogni settimana da un'azione di GitHub; il service worker ora prende prima la rete. Il vecchio indirizzo su Tophost mostra una pagina di trasferimento con redirect dopo 4 secondi. |
| 14/11/2026 | Tessere statiche come fonte principale: dentro la zona e con dati < 10 giorni nessuna chiamata a Overpass (che resta per fuori zona, dati vecchi o mancanti). |
| 15/11/2026 | **Statistiche dopo lo spostamento.** Sul sottodominio il percorso della pagina è `/` per tutte le app, quindi dal 14/11 le visite finivano mescolate in un'unica voce `/` di GoatCounter. Ora lo script in `index.html` mette `/nasone` davanti al percorso (`/nasone/`, `/nasone/storia.html`): la serie continua con lo stesso nome di quando l'app era su Tophost. Se la pagina è già sotto `/nasone/` (vecchio indirizzo) il nome non viene ripetuto. Eventi `nasone-installa-…` invariati. Provato in Chromium sul sottodominio con lo script vero di GoatCounter. |
