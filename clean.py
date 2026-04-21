import os
import re
import json
import pdfplumber

# --- CONFIGURATION DES CHEMINS ---
Input_data = r"C:/Users/user/Desktop/mon_projet_rag/document1.pdf"
Output_data = r"C:/Users/user/Desktop/mon_projet_rag/cleaned_data.txt"
output_json = r"C:/Users/user/Desktop/mon_projet_rag/cleaned_Ragdata.json"

def clean_strict_architecture(text):
    # 1. RECOLLAGE DES MOTS
    text = re.sub(r'(\w+)-\s*\n\s*(\w+)', r'\1\2', text)
    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)

    # 2. SUPPRESSION DE LA TABLE DES MATIÈRES / SOMMAIRE
    text = re.sub(r'(?m)^.*[\.\-_]{5,}.*$', '', text)
    text = re.sub(r'(?m)^.* [pP]\s*\d+\s*$', '', text)
    text = re.sub(r'(?m)^.*Investigations within Riparian Wetlands.*$', '', text)
    text = re.sub(r'(?m)^.*wetlands with different vegetation cover.*$', '', text)
    text = re.sub(r'(?m)^.*Ecosystem in Northwest France.*$', '', text)
    text = re.sub(r'(?i)^\s*SOMMAIRE\s*$', '', text, flags=re.MULTILINE)

    # 3. SUPPRESSION DES NUMÉROS DE PAGE ISOLÉS
    text = re.sub(r'(?m)^\s*\d+\s*$', '', text)
    text = re.sub(r'(?i)^\s*p(?:age)?\s*\d+\s*$', '', text)

    # 4. SUPPRESSION DES REMERCIEMENTS
    text = re.sub(r'(?i)REMERCIEMENTS[\s\S]*?J\'ai réussi à l\'écrire\. ;-?\)', '', text)
    text = re.sub(r'(?i)Ouf! Je peux enfin écrire cette page[\s\S]*?J\'ai réussi à l\'écrire\. ;-?\)', '', text)

    # 5. COUPURE DE LA BIBLIOGRAPHIE
    keywords = ["BIBLIOGRAPHIE", "REFERENCES BIBLIOGRAPHIQUES", "References"]
    for kw in keywords:
        if kw in text.upper():
            pos = text.upper().rfind(kw)
            text = text[:pos]
            break

    # 6. NETTOYAGE DU BRUIT ADMINISTRATIF (Page de garde et HAL)
    patterns_bruit = [
        # Bloc HAL (anglais et français)
        r'(?i)HAL is a multi-disciplinary[\s\S]*?privés\.',
        r'(?i)L’archive\s*ouverte\s*pluridisciplinaire\s*HAL[\s\S]*?privés\.',
        r'(?i)To cite this version:[\s\S]*?Français\.',
        r'(?i)HAL Id:.*?\n',
        r'(?i)https?://hal\.science/.*?\n',
        r'(?i)Submitted\s*on.*?\n',
        r'(?i)HAL\s*Authorization',
        
        # Bloc Jury et Administration
        r'(?i)N° Ordre : \d+',
        r'(?i)THESE\s+Présentée[\s\S]*?devant la commission d\'Examen',
        r'(?i)COMPOSITION DU JURY :[\s\S]*?(?=INTRODUCTION|SOMMAIRE|CHAPITRE|ABSTRACT|$)',
        r'(?i)Equipe d\'accueil :.*?\n',
        r'(?i)Ecole doctorale :.*?\n',
        r'(?i)Composante universitaire :.*?\n',
        r'⟨NNT:.*?⟩|⟨tel-.*?⟩'
    ]
    for p in patterns_bruit:
        text = re.sub(p, "", text, flags=re.MULTILINE)

    # 7. NORMALISATION DES ESPACES
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    return text.strip()

if __name__ == "__main__":
    print("Nettoyage approfondi en cours (Sommaire, Remerciements, HAL, Jury)...")
    
    try:
        with pdfplumber.open(Input_data) as pdf:
            full_text = ""
            for page in pdf.pages:
                content = page.extract_text()
                if content:
                    full_text += content + "\n\n"
        
        if not full_text.strip():
            print("⚠️ Le PDF est vide.")
        else:
            cleaned_content = clean_strict_architecture(full_text)

            # Sauvegarde en TXT
            with open(Output_data, "w", encoding="utf-8") as f:
                f.write(cleaned_content)
                
            # Sauvegarde en JSON pour le RAG
            rag_data = {"file": "document1.pdf", "content": cleaned_content}
            with open(output_json, "w", encoding="utf-8") as f:
                json.dump(rag_data, f, ensure_ascii=False, indent=4)

            print("\n✅ Succès : Le document a été nettoyé et préparé pour le RAG.")
            os.system(f'notepad.exe "{Output_data}"')

    except Exception as e:
        print(f"❌ Erreur : {e}")