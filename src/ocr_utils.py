# ocr_utils.py
import os
import subprocess
from pdf2image import convert_from_path
from PIL import Image, ImageOps

# -------------------------
# Função utilitária para salvar OCR em arquivo
# -------------------------
def save_ocr_text(pdf_path, ocr_text):
    """
    Salva OCR em arquivo .ocr.txt ao lado do PDF.
    """
    ocr_path = pdf_path.replace(".pdf", ".ocr.txt")
    with open(ocr_path, "w", encoding="utf-8") as f:
        f.write(ocr_text)
    return ocr_path

    
# -------------------------
# Função principal: OCR robusto com pré-processamento
# -------------------------
def pdf_to_text_preprocessed(pdf_path, dpi=400, lang="por", save_ocr_path=None):
    """
    Processa todas as páginas do PDF com pré-processamento:
    - escala de cinza
    - contraste automático
    - binarização leve
    Retorna o texto OCR concatenado.
    save_ocr_path: se fornecido, salva OCR final em arquivo.
    """
    texto_total = []
    pages = convert_from_path(pdf_path, dpi=dpi)

    for page_num, page in enumerate(pages):
        # Salvar página como PNG
        img_path = pdf_path.replace(".pdf", f"_page{page_num + 1}.png")
        page.save(img_path, "PNG")

        # Pré-processamento
        img = Image.open(img_path)
        img = img.convert("L")  # escala de cinza
        img = ImageOps.autocontrast(img, cutoff=1)
        img = img.point(lambda x: 0 if x < 150 else 255)  # binarização leve

        pre_img_path = img_path.replace(".png", "_pre.png")
        img.save(pre_img_path)
        print(f"Imagem pré-processada salva: {pre_img_path}")

        # OCR via subprocess
        output_file = img_path.replace(".png", "")
        cmd = [
            "tesseract",
            pre_img_path,
            output_file,
            "-l", lang,
            "--psm", "3",
            "--oem", "1"
        ]
        subprocess.run(cmd, check=True)

        # Ler texto OCR da página
        txt_path = f"{output_file}.txt"
        with open(txt_path, "r", encoding="utf-8") as f:
            page_text = f.read()
        texto_total.append(page_text)

    # Concatenar todas as páginas
    texto_final = "\n".join(texto_total)

    # Salvar OCR final se pedido
    if save_ocr_path:
        with open(save_ocr_path, "w", encoding="utf-8") as f:
            f.write(texto_final)
        print(f"OCR final salvo em: {save_ocr_path}")

    return texto_final
