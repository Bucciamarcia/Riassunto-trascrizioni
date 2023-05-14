# Riassunto Trascrizioni

Questo script prende la trascrizione di una riuniuone o altro audio (ad esempio un colloquio su Zoom o conferenza), e fa un riassunto delle parti importanti. Utilizza GPT (3.5 o 4) per leggere la trascrizione, e creare un riassunto o appunti di alta qualità.

## Video di introduzione

<a href="http://www.youtube.com/watch?feature=player_embedded&v=V6EW_woe57g
" target="_blank"><img src="http://img.youtube.com/vi/V6EW_woe57g/0.jpg" 
alt="IMAGE ALT TEXT HERE" width="240" height="180" border="10" /></a>

## Caratteristiche

- Lo script può usare sia gpt-3.5 che gpt-4. Consigliato gpt-4 per ottenere risultati migliori.
- Se la trascrizione è troppo lunga, lo script la divide automaticamente in parti. Quindi non c'è un limite alla lunghezza della trascrizione: si può tranquillamente inserire la trascrizione di una conferenza di 3 ore e lo script non dovrebbe avere problemi.

## Note importanti

- Lo script non vuole troncare frasi a metà per ottenere risultati di migliore qualità. Quindi cerca sempre un punto fermo per suddividere la trascrizione in parti. Questo significa che se il software di trascrizione non utilizza punteggiatura, lo script non funzionerà. Per questo, consiglio AWS Transcribe per la trascrizione e [aws-transcribe-transcript](https://github.com/trhr/aws-transcribe-transcript) per pulirla. Ma si può usare qualsiasi cosa, basta che la trascrizione abbia punteggiatura.
- GPT è in grado di creare riassunti anche da trascrizioni di bassa qualità, con parole sbagliate eccetera. Quindi non serve preoccuparsi troppo della qualità della trascrizione.
- Testato con Python 3.10.6, ma dovrebbe funzionare con qualsiasi versione recente.
- Ogni volta che si fa partire lo script, se è presente un output nel file `output.txt`, questo verrà cancellato. Quindi non dimenticarsi di salvare l'output da qualche parte prima di riutilizzare lo script!
- Come detto sopra, non c'è un limite alla lunghezza della trascrizione. Ma visto che questo script non gestisce gli errori, se ad esempio le API di GPT hanno dei problemi (come a volte succede), l'intero script si interromperà. È possibile andare a copiare l'output ottenuto fino a quel momento senza perdere niente e poi far ripartire lo script, ma servirà andare a cancellare la parte già elaborata in `trascrizione.txt` manualmente, se non si vuole ripartire da capo.

## Come usare Riassunto Trascrizioni

1. Installare i requisiti con `pip install -r requirements.txt`.
1. Rinominare `openaikey.txt.template` in `openaikey.txt` (togliere `.template`), e lì inserire la chiave API di OpenAI.
1. Rinominare `trascrizione.txt.template` in `trascrizione.txt` (togliere `.template`), e lì inserire la trascrizione della riunione o conferenza che si vuole riassumere.
1. Far partire lo script con `python main.py`.
1. Quando richiesto, digitare "1" o "2" (senza virgolette) per scegliere fra gpt-3.5 e gpt-4. Caldamente consigliato gpt-4.
1. Inserire l'argomento della conferenza o call. GPT riassumerà solo le parti che riguardano l'argomento della conferenza o call, e ignorerà le altre. Se ci sono più argomenti nella conferenza, si possono inserire tutti, ma sarebbe più opportuno dividerle manualmente (una parte per argomento), e usare questo script più volte per evitare di confondere GPT.
1. Una volta terminato lo script, il risultato sarà disponibile su `output.txt`.

## Contribuzioni

Se vuoi contribuire a questo progetto, sono sempre felice di avere una mano, quindi grazie per il tuo interesse! :)

Prima di creare un fork, apri una issue su Github per discutere di quello che vuoi cambiare o aggiungere.