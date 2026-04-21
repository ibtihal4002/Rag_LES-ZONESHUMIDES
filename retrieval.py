# Intégration recommandée pour l'endpoint /agentic
def hybrid_retrieval_logic(query, index, chunks):
    # Logique de décision (Maquette: Decision Path)
    decision = agent_router(query) 
    
    if decision == "bm25":
        # Action 1: Recherche par mots-clés (Systématique)
        return bm25_retrieval(chunks, query), "BM25"
    elif decision == "faiss":
        # Action 2: Recherche sémantique (Vectoriel RAG)
        return search(query, index, chunks), "FAISS"
    else:
        # Mode Hybride demandé en TP
        return "Combinaison des deux", "Hybrid"

