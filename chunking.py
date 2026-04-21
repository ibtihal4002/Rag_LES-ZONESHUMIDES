import re
import os
import sys

# 1. Fixed size
def chunk_fixed(text, size=100, overlap=20):
    words = text.split()
    chunks = []
    for i in range(0, len(words), size - overlap):
        chunk = " ".join(words[i:i + size])
        chunks.append(chunk)
    return chunks

# 2. Sentence based
def chunk_sentence(text):
    return re.split(r'(?<=[.!?]) +', text)

# 3. Paragraph based
def chunk_paragraph(text):
    return text.split("\n\n")

# 4. Sliding window
def chunk_sliding(text, window=120, step=60):
    words = text.split()
    chunks = []
    for i in range(0, len(words), step):
        chunk = " ".join(words[i:i + window])
        chunks.append(chunk)
    return chunks

# 5. Recursive splitting (AMÉLIORÉ)
def recursive_split(text, max_len=200):
    if len(text.split()) <= max_len:
        return [text]
    mid = len(text) // 2
    left = text[:mid]
    right = text[mid:]
    return recursive_split(left, max_len) + recursive_split(right, max_len)

# 6. Semantic (simplifié)
def semantic_chunk(text):
    return text.split(". ")

# 7. Token-based
def token_chunk(text, max_tokens=100):
    words = text.split()
    chunks = []
    for i in range(0, len(words), max_tokens):
        chunk = " ".join(words[i:i + max_tokens])
        chunks.append(chunk)
    return chunks

# 🔥 CHOIX AUTOMATIQUE
def choose_best_chunking(text):
    # Pour un projet PFA, le recursif est le plus robuste
    return recursive_split(text)

# ==========================================
# TEST UNIQUE (CORRIGÉ)
# ==========================================
if __name__ == "__main__":
    # On ajoute le dossier actuel au chemin système pour éviter les erreurs d'import
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.append(current_dir)

    try:
        # On importe depuis le BON nom de fichier : extract_text
        from extract_text import extract_and_clean_pdf 
        
        pdf_path = "document1.pdf"
        
        if os.path.exists(pdf_path):
            print(f"--- Tentative d'extraction sur {pdf_path} ---")
            text = extract_and_clean_pdf(pdf_path)
            chunks = choose_best_chunking(text)
            
            print("✅ TEST RÉUSSI")
            print(f"Nombre de chunks créés : {len(chunks)}")
            if len(chunks) > 0:
                print(f"Aperçu du premier chunk : {chunks[0][:150]}...")
        else:
            print(f"❌ Erreur : Le fichier {pdf_path} est introuvable dans {current_dir}")

    except ImportError as e:
        print(f"❌ Erreur d'importation : {e}")
        print("Vérifiez que votre fichier s'appelle exactement 'extract_text.py'")
    except Exception as e:
        print(f"❌ Une erreur est survenue : {e}")

