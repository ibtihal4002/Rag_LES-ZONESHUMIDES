import fitz  # PyMuPDF
import re

def extract_and_clean_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()

    # --- NETTOYAGE (Déjà très bien dans votre code) ---
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"-\s+", "", text)
    text = re.sub(r"HAL Id:.*|Submitted on.*", "", text)
    text = re.sub(r"\[\d+\]", "", text)
    text = re.sub(r"(Figure|Fig\.|Image)\s*\d+.*", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    
    return text

# 4. CHUNKING AMÉLIORÉ (Recursive-style)
def get_chunks(text, chunk_size=500, overlap=50):
    """
    Découpage plus intelligent pour le RAG
    """
    # Utilisation d'un délimiteur pour garder des phrases entières
    sentences = re.split(r'(?<=[.!?]) +', text)
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= chunk_size:
            current_chunk += " " + sentence
        else:
            if current_chunk: chunks.append(current_chunk.strip())
            # Gestion de l'overlap (chevauchement)
            current_chunk = sentence 

    if current_chunk:
        chunks.append(current_chunk.strip())
    
    # Filtrer les chunks trop courts (bruit)
    return [c for c in chunks if len(c) > 100]

# --- EXECUTION ---
path = "C:/Users/user/Desktop/mon_projet_rag/document1.pdf"
raw_text = extract_and_clean_pdf(path)
final_chunks = get_chunks(raw_text)

# Utile pour le bouton "Chunking" de la maquette
print(f"Extraction terminée : {len(final_chunks)} chunks créés.")
# 1. Sauvegarde dans un fichier
with open("verif_nettoyage.txt", "w", encoding="utf-8") as f:
    f.write(raw_text)

# 2. Commande pour ouvrir le fichier automatiquement (Windows)
import os
os.startfile("verif_nettoyage.txt")

print("Le document complet a été ouvert dans le bloc-notes pour vérification.")
