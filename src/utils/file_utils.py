import os


def save_text(texto: str, pdf_path: str, folder="ocr", suffix="") -> str:
    base_dir = os.path.dirname(pdf_path)
    ocr_dir = os.path.join(base_dir, folder)
    os.makedirs(ocr_dir, exist_ok=True)

    file_name = os.path.basename(pdf_path).replace(".pdf", f"{suffix}.ocr.txt")
    save_path = os.path.join(ocr_dir, file_name)

    with open(save_path, "w", encoding="utf-8") as f:
        f.write(texto)

    print(f"[OK] OCR salvo em: {save_path}")
    return save_path




def save_cleaner(texto: str, pdf_path: str, folder="ocr", suffix="") -> str:
    base_dir = os.path.dirname(pdf_path)
    ocr_dir = os.path.join(base_dir, folder)
    os.makedirs(ocr_dir, exist_ok=True)

    file_name = os.path.basename(pdf_path).replace(".pdf", f"{suffix}.ocr.txt")
    save_path = os.path.join(ocr_dir, file_name)

    with open(save_path, "w", encoding="utf-8") as f:
        f.write(texto)

    print(f"[OK] OCR salvo em: {save_path}")
    return save_path