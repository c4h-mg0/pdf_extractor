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
    
        save_text(paginas, pdf_path)
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


class ExtractRegex:
    def processar(self, blocos: list[str]) -> list[dict]:
        resultado_total = []
        for bloco in blocos:
            tipo = identificar_tipo(bloco)
            dados = {"tipo": tipo}

            # roda os extractors relevantes
            for extractor in BaseExtractor.registry:
                if tipo in extractor.tipos:
                    dados[extractor.campo] = extractor.extrair(bloco)

            # garante que todos os campos daquele tipo apareçam, mesmo se None
            obrigatorios = [
                e.campo for e in BaseExtractor.registry if tipo in e.tipos
            ]
            for campo in obrigatorios:
                if campo not in dados:
                    dados[campo] = None

            resultado_total.append(dados)
        return resultado_total


def identificar_tipo(texto: str) -> str:
    if "data consulta" in texto or "consulta" in texto:
        return "consulta"
    elif "data exame" in texto or "exame" in texto:
        return "exame"
    return "desconhecido"