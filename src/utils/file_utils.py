import os


def save_text(texto: str, pdf_path: str, folder: str = "ocr") -> str:
    """
    Salva o texto OCR em um .txt dentro de uma subpasta.
    """
    base_dir = os.path.dirname(pdf_path)         # pasta do PDF
    ocr_dir = os.path.join(base_dir, folder)     # subpasta 'ocr'
    os.makedirs(ocr_dir, exist_ok=True)          # cria se não existir

    file_name = os.path.basename(pdf_path).replace(".pdf", ".ocr.txt")
    save_path = os.path.join(ocr_dir, file_name)

    with open(save_path, "w", encoding="utf-8") as f:
        f.write(texto)

    print(f"[OK] OCR salvo em: {save_path}")
    return save_path
