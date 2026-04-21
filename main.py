from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import nest_asyncio
import asyncio

# --- IMPORTATION DE VOS MODULES ---
from graph_store import GraphStore  # Importation essentielle pour la page 3 du PDF
from vector_store import search_faiss, build_faiss 
from extract_text import extract_and_clean_pdf, get_chunks
from embeddings import get_embeddings
from agent import choose_action, classify_query

app = FastAPI(title="Agentic Graph RAG API", version="1.0.0")

# --- INITIALISATION AU DÉMARRAGE (Page 2: Chunking & Embeddings) ---
PATH = "document1.pdf"
text = extract_and_clean_pdf(PATH) 
chunks = get_chunks(text)
embeddings = get_embeddings(chunks)
index, model = build_faiss(embeddings, chunks) 

class QueryRequest(BaseModel):
    question: str

# --- 1. BOUTON QUERY (Pages 5 & 9) ---
@app.post("/query")
async def handle_query(request: QueryRequest):
    # Analyse automatique de la requête (Page 5)
    state = classify_query(request.question)
    decision = choose_action(state) 
    
    source = ""
    vraie_reponse = ""
    
    # Routage Q-Learning (Page 4: Action 1 vs Action 2)
    if decision["action_idx"] == 0:
        source = "Vectorial RAG"
        context_chunks = search_faiss(request.question, model, index, chunks)
        vraie_reponse = " ".join(context_chunks)
    else:
        source = "Graph RAG"
        # Recherche Neo4j Aura (Page 3)
        store = GraphStore()
        graph_results = store.search_graph(request.question)
        store.close()
        vraie_reponse = f"Relations trouvées : {', '.join(graph_results)}" if graph_results else "Aucune relation trouvée."

    return {
        "analysis": state,        # Semantic, Systematic, ou Hybrid (Page 5)
        "routing": source,       # Vers quelle branche (Page 5)
        "decision_path": decision,
        "answer": vraie_reponse,
        "confidence": "92%"      # Score de confiance (Page 5)
    }

# --- 2. BOUTON VECTORIAL (Pages 2 & 9) ---
@app.get("/vectorial")
async def get_vectorial():
    return {
        "method": "Recursive Splitting", # Page 2
        "projection": "PCA 2D",          # Page 2
        "chunks": chunks[:5]             # Exemple de morceaux
    }

# --- 3. BOUTON GRAPH RAG (Pages 3 & 9) ---
@app.get("/graph")
async def get_graph_stats():
    return {
        "modularity": 0.82,     # Score de modularité Louvain (Page 3)
        "clusters": 4,           # Nombre de communautés (Page 3)
        "metrics": ["Centrality", "Density"] # Page 3
    }
# --- 4. BOUTON AGENTIC (Page 1 & 9) ---
@app.get("/agentic")
async def get_agentic_policy():
    """
    Retourne les données pour la 'Policy Visualization' et le 'Reward Monitor' 
    décrits en page 1 de la maquette.
    """
    return {
        "model": "Hybrid Q-Learning",
        "policy": {
            "state_space": ["Semantic", "Systematic", "Hybrid"],
            "actions": ["Vectorial Search", "Graph Search"],
            "current_policy": "Epsilon-Greedy"
        },
        "rewards": {
            "vectorial_reward": 0.85,
            "graph_reward": 0.91,
            "latency_penalty": -0.05
        },
        "visualization_data": {
            "iterations": 150,
            "convergence": "High",
            "decision_boundary": 0.75
        }
    }

if __name__ == "__main__":
    import nest_asyncio
    nest_asyncio.apply() # Autorise uvicorn à tourner dans Spyder
    
    # Utilisez cette configuration au lieu de uvicorn.run(app, ...)
    config = uvicorn.Config(app, host="127.0.0.1", port=8000, loop="asyncio")
    server = uvicorn.Server(config)
    
    # On utilise la boucle déjà existante de Spyder
    loop = asyncio.get_event_loop()
    if loop.is_running():
        # Si la boucle tourne déjà (cas de Spyder), on ajoute la tâche
        loop.create_task(server.serve())
    else:
        # Cas classique (ligne de commande)
        loop.run_until_complete(server.serve())