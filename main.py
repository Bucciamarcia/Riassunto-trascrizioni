import openai
import tiktoken
import math
import re

def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.encoding_for_model(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

def split_transcription(transcription, split_num):
    # Split the transcription into sentences
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', transcription)

    # Calculate the target number of words per part
    total_words = sum(len(sentence.split()) for sentence in sentences)
    target_words_per_part = total_words // split_num

    # Split the sentences into parts
    parts = []
    current_part = []
    current_word_count = 0

    for sentence in sentences:
        sentence_word_count = len(sentence.split())

        if current_word_count + sentence_word_count <= target_words_per_part:
            current_part.append(sentence)
            current_word_count += sentence_word_count
        else:
            parts.append(" ".join(current_part))
            current_part = [sentence]
            current_word_count = sentence_word_count

    # Add the last part
    if current_part:
        parts.append(" ".join(current_part))

    return parts

def call_gpt(engine, argomento, parte):
    openai.api_key = openaikey

    completion = openai.ChatCompletion.create(
    model=engine,
    messages=[
        {"role": "system", "content": "Sei una superintelligenza artificiale. Il tuo compito è prendere appunti dettagliati di una conferenza."},
        {"role": "user", "content": f"- Il tuo nome è 'Segretaria AI'. Non fare mai riferimento al tuo nome.\n- Prendi appunti dettagliati e completi della trascrizione della conferenza qui sotto.\n- Il tuo obiettivo è creare un testo semplice da consultare, schematico e dettagliato, che permetta alle persone che non hanno partecipanto alla conferenza di apprendere tutto quello che è successo.\n- Riassumi solo le parti che parlano dell'argomento della conferenza, ignora tutto il resto.\n\nARGOMENTO DELLA CONFERENZA:\n\n{argomento}\n\nTRASCRIZIONE DELLA CONFERENZA:\n\n{parte}\n\nAPPUNTI DETTAGLIATI E COMPLETI:"},
    ],
    temperature=0
    )

    completion = completion.choices[0].message.content

    return completion

with open("openaikey.txt") as f:
    openaikey = f.read()

print("Scegli la versione di GPT da usare (consigliato gpt-4):")
print("1. gpt-3.5-turbo")
print("2. gpt-4")

usr_choice = input("Inserisci il numero corrispondente (1 o 2): ")

if usr_choice == "1":
    print("Hai scelto gpt-3.5-turbo")
    engine = "gpt-3.5-turbo"
    token_split = 2500
elif usr_choice == "2":
    print("Hai scelto gpt-4")
    engine = "gpt-4"
    token_split = 5000
else:
    print("Hai inserito un numero non valido. Chiusura in corso...")
    exit()

argomento = input("Inserisci l'argomento principale o gli argomenti della trascrizione (gli altri argomenti verranno ignorati. Premi invio quando hai finito): ")

# Open trascrizione.txt
with open("trascrizione.txt", "r") as f:
    trascrizione = f.read()

token_trascrizione = num_tokens_from_string(trascrizione, engine)

print(f"Numero di token della trascrizione: {token_trascrizione}")

if token_trascrizione < token_split:
    split_num = 1
else:
    # Round up
    split_num = math.ceil(token_trascrizione // token_split)

print(f"Diviso la trascrizione in {split_num + 1} parte/i...")

with open("output.txt", "w", encoding="utf-8") as f:
    f.write("")

# Write the file
parts = split_transcription(trascrizione, split_num)
for i, part in enumerate(parts):
    print(f"Riassumendo parte {i + 1}...")
    riassunto = call_gpt(engine, argomento, part)
    print(f"Riassunto parte {i + 1} completato. Scrivendo il file...")
    with open("output.txt", "a", encoding="utf-8") as f:
        f.write(f"PARTE {i + 1}:\n\n")
        f.write(riassunto)
        f.write("\n\n")
    print(f"Scrittura parte {i + 1} completata.")