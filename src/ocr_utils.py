# ocr_utils.py
import os
from pdf2image import convert_from_path
from PIL import Image, ImageOps
import pytesseract


def pdf_to_text_preprocessed(pdf_path, dpi=400, lang="por", save_ocr_path=None):
    texto_total = []
    pages = convert_from_path(pdf_path, dpi=dpi)

    for page_num, page in enumerate(pages):
        # Pré-processamento em memória
        img = page.convert("L")
        img = ImageOps.autocontrast(img, cutoff=1)
        img = img.point(lambda x: 0 if x < 150 else 255)

        # OCR direto com pytesseract
        page_text = pytesseract.image_to_string(img, lang=lang, config="--psm 6 --oem 1")
        texto_total.append(page_text)

    texto_final = "\n".join(texto_total)

    if save_ocr_path:
        with open(save_ocr_path, "w", encoding="utf-8") as f:
            f.write(texto_final)
        print(f"OCR final salvo em: {save_ocr_path}")

    return texto_final
