# src/parse_steps/pipeline_parser.py
from src.ocr.pdf_ocr import PdfOCR
from src.interfaces import Step, BaseExtractor
from src.parsers.cleaners import *
import re

from src.utils.file_utils import save_text


class RunOcr(Step):
    def __init__(self, dpi=400, lang="por"):
        self.dpi = dpi
        self.lang = lang

    def processar(self, pdf_path: str) -> list[str]:
        ocr_engine = PdfOCR(dpi=self.dpi, lang=self.lang)
        paginas = ocr_engine.extract(pdf_path)
        
        # Salva para debug: cada página num arquivo separado
        for i, texto in enumerate(paginas, start=1):
            save_text(texto, pdf_path, folder="ocr", suffix=f"_p{i}")

        return paginas


class Cleaner(Step):     
    def processar(self, paginas: list[str]) -> list[str]:
        paginas_limpas = []
        for texto in paginas:
            texto = remover_invisiveis(texto)
            texto = remover_acentos(texto)
            texto = texto_lower(texto)
            texto = ajustar_espacos(texto)
            paginas_limpas.append(texto)
        return paginas_limpas



class ExtractRegex(Step):
    def processar(self, blocos: list[str]) -> list[dict]:
        # Recebe blocos já separados e aplica regex para extrair campos.
        
        resultado_total = []

        for bloco in blocos:
            dados = {}
            for extractor in BaseExtractor.registry:
                dados[extractor.campo] = extractor.extrair(bloco)
            resultado_total.append(dados)
        return resultado_total  


