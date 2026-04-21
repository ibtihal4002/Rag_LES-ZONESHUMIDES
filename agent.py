import random

# Q-table : Actions [0: Vectorial, 1: Graph]
Q_table = {
    "semantic": [0.5, 0.2],   # Priorité initiale au Vectoriel pour le sémantique
    "systematic": [0.2, 0.5]  # Priorité initiale au Graphe pour les relations
}

def classify_query(query):
    query = query.lower()
    # Mots-clés pour le Graphe (Systematic/Relational)
    graph_keywords = ["relation", "lien", "connecté", "influence", "chemin", "communauté", "centralité"]
    
    if any(word in query for word in graph_keywords):
        return "systematic"
    return "semantic"

def choose_action(state, epsilon=0.1):
    # Logique Epsilon-Greedy (Exploration vs Exploitation)
    if random.random() < epsilon:
        action = random.choice([0, 1]) # Explore
    else:
        action = Q_table[state].index(max(Q_table[state])) # Exploite
    
    # Calcul d'un score de confiance (basé sur la valeur Q)
    confiance = round(max(Q_table[state]) * 100, 2)
    
    return {
        "action_idx": action,
        "action_name": "Graph RAG" if action == 1 else "Vectorial RAG",
        "state": state,
        "confidence": f"{confiance}%"
    }

def update_q(state, action, reward):
    alpha = 0.1  # Taux d'apprentissage
    # Formule Bellman simplifiée pour le projet
    Q_table[state][action] += alpha * (reward - Q_table[state][action])

