from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Initialisation du modèle (Génération)
model = SentenceTransformer('all-MiniLM-L6-v2')

def process_vectorial_rag(chunks):
    # 1. Création des embeddings (Code 2)
    embeddings = model.encode(chunks).astype("float32")
    
    # 2. Création de l'index FAISS (Code 1)
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)
    
    return index, embeddings

# Contenu de embeddings.py
from sentence_transformers import SentenceTransformer

# On charge le modèle une seule fois pour tout le projet
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embeddings(chunks):
    """Transforme une liste de textes en vecteurs numériques"""
    if not chunks:
        return []
    embeddings = model.encode(chunks)
    return embeddings
def search_faiss(question, model, index, chunks, k=3):
    # 1. Transformer la question en vecteur
    query_vector = model.encode([question]).astype('float32')
    
    # 2. Chercher les k morceaux les plus proches dans l'index FAISS
    distances, indices = index.search(query_vector, k)
    
    # 3. Récupérer les textes correspondants
    results = [chunks[i] for i in indices[0]]
    return results
