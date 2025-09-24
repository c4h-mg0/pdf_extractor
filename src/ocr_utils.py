# ocr_utils.py
import os
from pdf2image import convert_from_path
from PIL import Image, ImageOps
import pytesseract
import fitz
import io



def pdf_ocr_text(pdf_path, dpi=400, lang="por"):
    texto_total = []
    doc = fitz.open(pdf_path)

    for page_num, page in enumerate(doc):
        rect = page.rect
        top40 = fitz.Rect(0, 0, rect.width, rect.height * 0.4)

        # Renderizar só a área cortada
        pix = page.get_pixmap(clip=top40, dpi=dpi)
        img = Image.open(io.BytesIO(pix.tobytes("png")))

        # Pré-processamento
        img = img.convert("L")
        img = ImageOps.autocontrast(img, cutoff=1)
        img = img.point(lambda x: 0 if x < 145 else 255)

        # OCR
        page_text = pytesseract.image_to_string(img, lang=lang, config="--psm 6 --oem 1")
        texto_total.append(page_text)

    doc.close()
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



