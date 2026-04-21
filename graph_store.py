from neo4j import GraphDatabase
from transformers import pipeline

# ===== CONFIGURATION NEO4J AURA =====
URI = "neo4j+s://91b1b7ea.databases.neo4j.io"
USER = "91b1b7ea"
PASSWORD = "r83VmmnZvK23h4PdmuC7dT5YthPKCmhR90eHlvn-KYE"

class GraphStore:
    def __init__(self):
        # Correction : utilisation de aggregation_strategy à la place de grouped_entities
        self.driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
        self.ner = pipeline("ner", aggregation_strategy="simple", model="dbmdz/bert-large-cased-finetuned-conll03-english")

    def close(self):
        self.driver.close()

    def extract_entities(self, text):
        """Extrait les entités et filtre par score de confiance"""
        entities = self.ner(text)
        # On ne garde que les entités avec un score de confiance élevé (> 0.80)
        # On utilise ent['entity_group'] car aggregation_strategy change la structure du dictionnaire
        return list(set([ent["word"] for ent in entities if ent.get('score', 0) > 0.80]))

    def create_graph(self, chunks):
        """Crée des noeuds Entités et des relations basées sur les chunks"""
        with self.driver.session() as session:
            for chunk in chunks:
                entities = self.extract_entities(chunk)
                if len(entities) < 2: continue

                # 1. Créer les noeuds d'entités (Optimisé en une seule passe)
                for ent in entities:
                    session.run("MERGE (e:Entity {name: $name})", name=ent)

                # 2. Créer les relations RELATED
                for i in range(len(entities)):
                    for j in range(i + 1, len(entities)):
                        session.run("""
                            MATCH (a:Entity {name: $e1}), (b:Entity {name: $e2})
                            WHERE a.name <> b.name
                            MERGE (a)-[:RELATED]-(b)
                        """, e1=entities[i], e2=entities[j])
        print("✅ Graphe peuplé avec succès !")

    def search_graph(self, query_term):
        """Recherche dans le graphe pour le bouton Graph RAG"""
        query = """
        MATCH (e:Entity)-[:RELATED]-(neighbor)
        WHERE e.name CONTAINS $term
        RETURN neighbor.name as link
        LIMIT 5
        """
        with self.driver.session() as session:
            result = session.run(query, term=query_term)
            return [record["link"] for record in result]

# ===== TEST DU MODULE =====
if __name__ == "__main__":
    try:
        store = GraphStore()
        # Test avec un exemple concret tiré de votre document
        test_chunks = ["La dénitrification dans les zones humides réduit les flux de nitrate."]
        store.create_graph(test_chunks)
        print("✅ Connexion et création réussies !")
        
        # Test de recherche
        links = store.search_graph("nitrate")
        print(f"Relations trouvées pour 'nitrate' : {links}")
        
        store.close()
    except Exception as e:
        print(f"❌ Erreur : {e}")

