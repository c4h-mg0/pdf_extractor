import os
import json
from src.pdf_processor import process_pdf

BASE_DIR = "Meus_pdfs"

def process_all_folders(base_dir=BASE_DIR):
    """
    Vasculha todas as subpastas dentro de base_dir,
    processa os PDFs e salva resultados.json em cada subpasta.
    """
    for root, dirs, files in os.walk(base_dir):
        # Apenas entrar em subpastas diretas (ignora a raiz)
        if root == base_dir:
            for subpasta in dirs:
                subpath = os.path.join(base_dir, subpasta)
                process_one_subfolder(subpath, subpasta)


def process_one_subfolder(subpath, subpasta):
    """
    Processa os PDFs de uma única subpasta e salva o JSON dentro dela.
    """
    resultados = []
    for fname in os.listdir(subpath):
        if fname.lower().endswith(".pdf"):
            pdf_path = os.path.join(subpath, fname)
            dados = process_pdf(pdf_path)
            # Marca a subpasta, não a pasta raiz
            for d in dados:
                d["pasta"] = subpasta
            resultados.extend(dados)

    # Salva JSON dentro da própria subpasta
    if resultados:
        out_path = os.path.join(subpath, "resultados.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(resultados, f, ensure_ascii=False, indent=2)
        print(f"[OK] Extração salva em {out_path}")


if __name__ == "__main__":
    process_all_folders()
