from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# 1. Calcul de la confiance pour l'affichage Maquette
def calculate_confidence(query_emb, doc_embs):
    if not doc_embs: return 0.0
    # Similarité entre la question et les documents trouvés
    similarities = cosine_similarity([query_emb], doc_embs)
    confidence = np.mean(similarities)
    return round(confidence * 100, 2)

# 2. Calcul du REWARD pour le Q-Learning (Hybrid Feedback Loop)
def get_agent_reward(retrieved_docs, relevant_docs, confidence_score):
    # On combine la précision et la confiance sémantique
    k = len(retrieved_docs)
    prec = len(set(retrieved_docs) & set(relevant_docs)) / k if k > 0 else 0
    
    # La récompense est un mélange de précision et de qualité sémantique
    reward = (0.7 * prec) + (0.3 * (confidence_score / 100))
    return reward

# 3. Vos métriques existantes (utiles pour les logs techniques)
def precision_at_k(retrieved, relevant, k=5):
    retrieved_k = retrieved[:k]
    intersect = set(retrieved_k) & set(relevant)
    return len(intersect) / k

def recall_at_k(retrieved, relevant):
    if not relevant: return 0
    intersect = set(retrieved) & set(relevant)
    return len(intersect) / len(relevant)

