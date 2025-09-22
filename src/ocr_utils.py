# ocr_utils.py
import os
import cv2
import numpy as np
from pdf2image import convert_from_path
from PIL import Image, ImageOps
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"/usr/bin/tesseract"

def detectar_angulo(img, min_angle):
    """
    Detecta o ângulo de rotação de uma imagem usando HoughLines.
    Retorna o ângulo (em graus). Se não houver linhas relevantes, retorna 0.
    """
    # Binariza para detecção de linhas
    _, binary = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Detecta bordas
    edges = cv2.Canny(binary, 50, 150, apertureSize=3)

    # Hough para linhas
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 100)

    if lines is not None:
        angles = [(theta * 180 / np.pi) - 90 for rho, theta in lines[:, 0]]
        median_angle = np.median(angles)
        if abs(median_angle) >= min_angle:
            return median_angle

    return 0.0


def corrigir_rotacao(img, angle):
    """
    Corrige a rotação de uma imagem em tons de cinza usando warpAffine.
    """
    if angle == 0:
        return img
    (h, w) = img.shape[:2]
    M = cv2.getRotationMatrix2D((w // 2, h // 2), angle, 1.0)
    return cv2.warpAffine(img, M, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)


def ocr_imagem(img, lang):
    """
    Executa OCR em uma imagem numpy (grayscale).
    Retorna o texto reconhecido.
    """
    pil_img = Image.fromarray(img)
    pil_img = ImageOps.autocontrast(pil_img, cutoff=1)
    return pytesseract.image_to_string(pil_img, lang=lang, config="--psm 6 --oem 1")


def pdf_ocr_text(pdf_path, dpi=300, lang="por", min_angle=9.0):
    """
    Faz OCR em PDFs, corrigindo rotações pequenas (± min_angle).
    """
    pages = convert_from_path(pdf_path, dpi=dpi)
    texto_total = []

    for page in pages:
        # Converte para array OpenCV (tons de cinza)
        img = np.array(page.convert("L"))

        # Detecta ângulo
        angle = detectar_angulo(img, min_angle=min_angle)

        # Corrige rotação se necessário
        img = corrigir_rotacao(img, angle)

        # OCR final
        page_text = ocr_imagem(img, lang=lang)
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



