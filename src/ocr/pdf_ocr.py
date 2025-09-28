import io
import fitz
import pytesseract
from PIL import Image
from src.ocr.image_preprocess import preprocess_image
from src.utils.file_utils import save_text


class PdfOCR:
    def __init__(self, dpi=400, lang="por"):
        """
        Classe para extração de texto via OCR em PDFs.
        :param dpi: resolução para renderizar as páginas
        :param lang: idioma do OCR (ex: 'por', 'eng')
        """
        self.dpi = dpi
        self.lang = lang

    def extract(self, pdf_path: str) -> str:
        """
        Extrai texto do PDF (OCR aplicado no top 40% de cada página).
        Retorna o texto concatenado.
        """
        texto_total = []
        doc = fitz.open(pdf_path)

        for page_num, page in enumerate(doc):
            rect = page.rect
            top40 = fitz.Rect(0, 0, rect.width, rect.height * 0.4)

            # Renderizar só a área cortada
            pix = page.get_pixmap(clip=top40, dpi=self.dpi)
            img = Image.open(io.BytesIO(pix.tobytes("png")))

            # Pré-processamento
            img = preprocess_image(img)

            # OCR
            page_text = pytesseract.image_to_string(
                img,
                lang=self.lang,
                config="--psm 6 --oem 1"
            )
            texto_total.append(page_text)

        doc.close()
        return texto_total

    def save(self, texto: str, pdf_path: str, folder: str = "ocr") -> str:
        """
        Salva o OCR em arquivo .txt dentro de uma subpasta.
        """
        return save_text(texto, pdf_path, folder=folder)
