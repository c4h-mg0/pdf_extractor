import os
import json
from src.pipeline.processor_pipeline import process_pdf
from src.pipeline.helpers import consolidar_resultados, consolidar_firestore
# from src.cleaning.data_cleaner import deduplicate_records

BASE_DIR = "meus_pdfs"


def process_all_folders(base_dir=BASE_DIR):
    all_records = []
    stats = {}

    # Percorre subpastas da pasta base
    for root, dirs, files in os.walk(base_dir):
        if root == base_dir:
            for subpasta in dirs:
                subpath = os.path.join(base_dir, subpasta)
                records, n_pdfs = process_one_subfolder(subpath, subpasta)
                all_records.extend(records)
                stats[subpasta] = {
                    "pdfs": n_pdfs,
                    "docs": len(records)
                }

    # Deduplicação global com log e estatísticas
    # final_records = deduplicate_records(
    #     all_records,
    #     log_path=os.path.join(base_dir, "fix.txt"),
    #     stats=stats
    # )

    # Salva consolidado
    # out_path = os.path.join(base_dir, "firestore.json")
    # with open(out_path, "w", encoding="utf-8") as f:
    #     json.dump(final_records, f, ensure_ascii=False, indent=2)
    # print(f"[OK] Arquivo consolidado salvo em {out_path}")


def process_one_subfolder(subpath, subpasta):
    """
    Processa todos os PDFs dentro de uma subpasta.
    - Chama process_pdf() para cada arquivo.
    - Salva resultados parciais em resultados.json
    """
    resultados = []
    n_pdfs = 0

    for fname in os.listdir(subpath):
        if fname.lower().endswith(".pdf"):
            n_pdfs += 1
            pdf_path = os.path.join(subpath, fname)
            dados = process_pdf(pdf_path)
            resultados.extend(dados)

    if resultados:
        out_path = os.path.join(subpath, "resultados.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(resultados, f, ensure_ascii=False, indent=2)
        print(f"[OK] Extração salva em {out_path}")

    return resultados, n_pdfs


if __name__ == "__main__":
    process_all_folders()
    consolidar_resultados(BASE_DIR)
    consolidar_firestore(BASE_DIR)
