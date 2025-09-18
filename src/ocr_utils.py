import pytesseract
from pdf2image import convert_from_path

# Ajuste o caminho se necessário
pytesseract.pytesseract.tesseract_cmd = r"/usr/bin/tesseract"

def pdf_to_text(pdf_path, lang="por"):
    """
    Converte um PDF em texto via OCR.
    Pula páginas em branco automaticamente.
    """
    pages = convert_from_path(pdf_path, dpi=300)
    texto_total = []

    for page in pages:
        text = pytesseract.image_to_string(page, lang=lang).strip()
        if text:  # ignora páginas sem conteúdo
            texto_total.append(text)

    return "\n".join(texto_total)
