import os

import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv

load_dotenv()


functie_embedding = embedding_functions.OpenAIEmbeddingFunction(
    api_key=os.getenv("OPENAI_API_KEY"),
    model_name="text-embedding-3-small",
)

client = chromadb.Client()

colectie = client.create_collection(
    name="s50_lectii",
    embedding_function=functie_embedding,
)


def indexeaza_lectie(lectie):
    colectie.add(
        ids=[str(lectie.id)],
        documents=[lectie.continut],
        metadatas=[{"titlu": lectie.titlu}]
    )


def indexeaza_toate(lectii):
    for lectie in lectii:
        indexeaza_lectie(lectie)

    print(f"Index RAG: {colectie.count()} lectii.")


def sterge_din_index(lectie_id):
    colectie.delete(ids=[str(lectie_id)])


def cauta(intrebare, n_rezultate=2):
    if colectie.count() == 0:
        return []

    rezultat = colectie.query(
        query_texts=[intrebare],
        n_results=n_rezultate
    )

    texte = rezultat["documents"][0]
    metadatas = rezultat["metadatas"][0]
    distante = rezultat["distances"][0]

    lista = []

    for i in range(len(texte)):
        lista.append({
            "titlu": metadatas[i]["titlu"],
            "text": texte[i],
            "distanta": round(distante[i], 3)
        })

    return lista
