import os
from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.docstore.document import Document
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import TokenTextSplitter

print("Scegli la versione di GPT da usare (consigliato gpt-4):")
print("1. gpt-3.5-turbo")
print("2. gpt-4")

usr_choice = input("Inserisci il numero corrispondente (1 o 2): ")

if usr_choice == "1":
    print("Hai scelto gpt-3.5-turbo")
    engine = "gpt-3.5-turbo"
    chunk_size = 2500
elif usr_choice == "2":
    print("Hai scelto gpt-4")
    engine = "gpt-4"
    chunk_size = 5000
else:
    print("Hai inserito un numero non valido. Chiusura in corso...")
    exit()

argomento = input("Inserisci l'argomento principale o gli argomenti della trascrizione (gli altri argomenti verranno ignorati. Premi invio quando hai finito): ")

with open("openaikey.txt") as f:
    openaikey = f.read()

os.environ["OPENAI_API_KEY"] = openaikey

llm = ChatOpenAI(temperature=0, client=engine)

text_splitter = TokenTextSplitter(chunk_size=chunk_size, chunk_overlap=50)

# Apri trascrizione.txt
with open("trascrizione.txt", "r") as f:
    trascrizione = f.read()

# Dividi il documento in parti
texts = text_splitter.split_text(trascrizione)

docs = [Document(page_content=t) for t in texts]

# Personalizza il prompt di Langchain con l'argomento della conferenza messo in input

prompt_argomento = PromptTemplate(
    input_variables=["argomento", "text"],
    template="""- Sei un'intelligenza artificiale che prende appunti dettagliati e completi della trascrizione di una conferenza.
- Il tuo obiettivo è creare un testo semplice da consultare, schematico e dettagliato, che permetta alle persone che non hanno partecipanto alla conferenza di avere tutte le informazioni, come se fossero state presenti.
- Riassumi solo le parti che parlano dell'argomento della conferenza, ignora tutto il resto.
- Questa è solo la prima iterazione del riassunto, quindi è molto meglio essere troppo dettagliati piuttosto che troppo poco: è importante includere tutte le informazioni che potrebbero risultare utili in futuro, anche se non sei sicuro.

TRASCRIZIONE DELLA CONFERENZA:

{text}

ARGOMENTO DELLA CONFERENZA:

{argomento}

RIASSUNTO ESTESO:"""
)

prompt_template = prompt_argomento.format(argomento=argomento, text="{text}")

PROMPT = PromptTemplate(template=prompt_template, input_variables=["text"])
refine_template = (
    "Il tuo lavoro è di creare un riassunto finale, completo ed esteso, delle note di una conferenza.\n"
    "Ti abbiamo fornito un sommario esistente fino a questo punto:\n\n{existing_answer}\n\n"
    "Ora abbiamo l'opportunità di migliorare questo sommario esistente"
    "(solo se necessario) con più contesto qui sotto.\n"
    "------------\n"
    "{text}\n"
    "------------\n"
    "Dato il nuovo contesto, migliora il sommario esistente."
    "Se il contesto non è utile, riscrivi il sommario originale esattamente così com'è."
    "Il tuo lavoro è solo direndere il riassunto più leggibile. Non omettere mai niente: includi sempre tutte le informazioni."
    "Se opportuno, usa paragrafi, elenchi puntati e numerati, per  rendere il riassunto più leggibile."
)
refine_prompt = PromptTemplate(
    input_variables=["existing_answer", "text"],
    template=refine_template,
)
chain = load_summarize_chain(llm, chain_type="refine", return_intermediate_steps=False, question_prompt=PROMPT, refine_prompt=refine_prompt)
output_finale = chain({"input_documents": docs}, return_only_outputs=True) # Questo fa partire il processo di riassunto

# Salva il risultato in un file
with open("output.txt", "w", encoding="utf-8") as f:
    f.write(output_finale["output_text"])