# ocr_utils.py
import os
from pdf2image import convert_from_path
from PIL import Image, ImageOps
import pytesseract


def pdf_ocr_text(pdf_path, dpi=300, lang="por"):
    """Converte PDF em texto via OCR, com pré-processamento."""
    texto_total = []
    pages = convert_from_path(pdf_path, dpi=dpi)

    for page_num, page in enumerate(pages):
        # Pré-processamento
        img = page.convert("L")
        img = ImageOps.autocontrast(img, cutoff=1)
        img = img.point(lambda x: 0 if x < 140 else 255)

        # OCR
        page_text = pytesseract.image_to_string(
            img, lang=lang, config="--psm 6 --oem 1"
        )
        texto_total.append(page_text)

    return "\n".join(texto_total)


def save_ocr_txt(texto, pdf_path, folder="ocr"):
    """Salva o OCR em um .txt dentro de uma subpasta 'ocr' na mesma pasta dos PDFs."""
    base_dir = os.path.dirname(pdf_path)         # pasta do PDF
    ocr_dir = os.path.join(base_dir, folder)     # subpasta 'ocr'
    os.makedirs(ocr_dir, exist_ok=True)          # cria se não existir

    file_name = os.path.basename(pdf_path).replace(".pdf", ".ocr.txt")
    save_path = os.path.join(ocr_dir, file_name)

    with open(save_path, "w", encoding="utf-8") as f:
        f.write(texto)

    print(f"OCR final salvo em: {save_path}")
    return save_path



