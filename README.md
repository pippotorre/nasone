# Nasone — la fontanella di Roma più vicina

Web app (installabile come app su Android e iPhone) che trova il **nasone** — la fontanella romana in ghisa con il «naso» curvo — più vicino alla tua posizione e disegna il percorso a piedi per raggiungerlo. Ha una pagina di **storia e curiosità** sui nasoni (`storia.html`).

È la sorella di [Turet](https://github.com/pippotorre/turet) (le fontanelle di Torino): stesso motore, altra città, altra grafica (porpora, ghisa e travertino) e altri testi.

## Cosa fa
- Rileva la posizione (GPS del telefono) oppure, se rifiuti o non c'è, ti lascia toccare la mappa per indicare dove sei.
- Cerca i punti d'acqua potabile attorno a te in OpenStreetMap a partire da 1 km; con «Cerca più lontano» si estende a 2, 3,5 e 5 km. Mostra il più vicino e gli altri (fino a 12 in lista, 10 sulla mappa).
- Disegna il percorso a piedi con distanza, tempo e indicazioni passo passo nella lingua scelta; se il servizio dei percorsi non risponde mostra la linea d'aria.
- Pulsanti per proseguire con Google Maps (e Mappe di Apple su iPhone/iPad).
- Lingue: italiano, inglese, francese, spagnolo, tedesco.
- Funziona offline in parte: l'app si apre e ricorda gli ultimi risultati per la zona (7 giorni); mappe e percorsi richiedono internet.

## Pubblicazione
Il sito è statico e si pubblica su **GitHub Pages** all'indirizzo `https://nasone.entratadisicurezza.com/` (workflow `.github/workflows/pubblica.yml`, impostazione una tantum in [docs/PAGES.md](docs/PAGES.md)). Non servono PHP, database o chiavi.
Per aggiornare dopo una modifica a CSS/JS cambia il numero `?v=` in `index.html` e in `sw.js`, e `VERSION` in `sw.js`: il service worker prende comunque prima la rete, quindi gli utenti online vedono subito la versione nuova.

## Struttura
- `index.html`, `css/app.css`, `js/app.js` (interfaccia e flusso), `js/geo.js` (funzioni pure: distanze, query, istruzioni), `js/i18n.js` (traduzioni IT/EN/FR/ES/DE), `storia.html`, `privacy.html`.
- `vendor/leaflet/` — Leaflet 1.9.4 (licenza BSD-2), niente CDN.
- `manifest.webmanifest`, `sw.js`, `img/` — installazione come app e icone.
- `data/t/` — tessere di dati generate dal workflow; `.github/workflows/pubblica.yml` — pubblicazione e aggiornamento settimanale.
- `test/` — prove senza dipendenze: `node test/geo.test.js && node test/i18n.test.js`.
- `art/` — illustrazione del nasone (`nasone.svg`) e script che genera icone e grafica dello store (`python3 art/build.py`, richiede Playwright).
- `store/`, `docs/`, `tools/` — materiali, guida completa per Google Play ([docs/ANDROID.md](docs/ANDROID.md)) e controllo del sito (`bash tools/verifica-sito.sh URL`).

## Dati e servizi
I punti d'acqua potabile sono quelli di OpenStreetMap (`amenity=drinking_water`, anche come aree, più le `amenity=fountain` con `drinking_water=yes`). L'app è completa quanto lo è la mappatura: se manca una fontanella, si aggiunge su openstreetmap.org e compare in app senza altre modifiche.

| Servizio | A cosa serve | Note |
| --- | --- | --- |
| OpenStreetMap (tile.openstreetmap.org) | mappa | Uso leggero consentito con attribuzione ([policy](https://operations.osmfoundation.org/policies/tiles/)). Con molti utenti serve un fornitore di tile dedicato. |
| Overpass (overpass-api.de, overpass.private.coffee, overpass.kumi.systems, overpass.openstreetmap.fr) | posizione delle fontanelle | Gratuito, uso corretto. L'app li interroga in parallelo (secondo tentativo su 502/429) e usa il primo che risponde; invia un punto arrotondato a ~100 m. |
| routing.openstreetmap.de (profilo a piedi) | percorso | Gratuito, senza garanzie. In caso di errore l'app ripiega sulla linea d'aria. |

## Affidabilità dei dati
- L'app scarica **una volta** le fontanelle di un'area di circa 6,5 km attorno a te (a «tessere» di ~2 km) e le tiene nel telefono: la copia è considerata fresca per 3 giorni, e fino a 60 giorni viene usata se i server non rispondono. «Cerca più lontano» filtra in locale, senza altre richieste.
- I server Overpass vengono interrogati a scaglioni (il primo subito, gli altri solo se tardano), non tutti insieme.
- **Dati pronti (`data/t/`):** ogni lunedì un'azione di GitHub scarica da OpenStreetMap le fontanelle della zona con `node tools/genera-tessere.mjs` e le salva in piccoli file a griglia di 0,25° (`data/t/<riga>_<colonna>.json`, più `index.json`). L'app li carica per primi: i risultati arrivano subito e restano disponibili anche se i server pubblici sono fuori uso; i server pubblici aggiungono poi le novità.

## Privacy
La posizione non viene salvata né inviata a un server del progetto: resta nel browser. Ai servizi esterni vanno solo un punto arrotondato (ricerca) e le due coordinate del tragitto (percorso). Nel browser si salvano la lingua e la copia degli ultimi risultati (localStorage, chiavi `nasone.*`).

## Storia e curiosità
I testi di `storia.html` sono tratti da [Turismo Roma](https://www.turismoroma.it/it/page/i-nasoni-le-fontanelle-di-roma) e [Romeing](https://romeing.it/nasoni-romes-democracy-of-water); misure e dettagli variano da una fonte all'altra.

## Aggiungere una lingua
Copia un blocco in `DICT` di `js/i18n.js`, traduci i valori (`{segnaposto}` invariati), aggiungi il codice a `LANGS`, un pulsante `data-lang` in `index.html` e una sezione in `storia.html` e `privacy.html`. `node test/i18n.test.js` controlla le chiavi mancanti.
