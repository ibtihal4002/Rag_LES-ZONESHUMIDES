import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# 1. Renommé en 'build_faiss' pour correspondre à l'import de votre main.py
def build_faiss(embeddings, chunks):
    # Initialisation du modèle (nécessaire pour search_faiss plus tard)
    model = SentenceTransformer("all-MiniLM-L6-v2")
    
    # Indispensable pour éviter les erreurs de type dans FAISS
    embeddings = np.array(embeddings).astype("float32")
    
    # Récupération automatique de la dimension
    dim = embeddings.shape[1]
    
    # Utilisation de IndexFlatL2 comme demandé (Page 2 de votre PDF)
    index = faiss.IndexFlatL2(dim)
    
    # Ajout des vecteurs
    index.add(embeddings)
    
    return index, model

# 2. Votre fonction de recherche
def search_faiss(query, model, index, chunks, k=3):
    # 1. Transformer la question en vecteur
    query_embedding = model.encode([query])
    
    # 2. Rechercher dans l'index FAISS
    distances, indices = index.search(query_embedding.astype('float32'), k)
    
    # 3. Récupérer les morceaux de texte correspondants
    results = [chunks[i] for i in indices[0] if i < len(chunks)]
    return results