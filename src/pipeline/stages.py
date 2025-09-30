# src/pipeline/stages.py
from src.ocr.pdf_ocr import PdfOCR
from src.interfaces import Step, BaseExtractor
from src.parsers.cleaners import *
from src.pipeline.helpers import identificar_tipo, save_to_file


class RunOcr(Step):
    def __init__(self, dpi=400, lang="por"):

        self.dpi = dpi
        self.lang = lang

    def processar(self, pdf_path: str) -> list[str]:
        ocr_engine = PdfOCR(dpi=self.dpi, lang=self.lang)
        paginas = ocr_engine.extract(pdf_path)
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


class SaveStep(Step):
    def __init__(self, prefix="stage", folder="debug"):
        self.prefix = prefix
        self.folder = folder

    def processar(self, data):
        save_to_file(data, prefix=self.prefix, folder=self.folder)
        return data  # importante: não altera o fluxo
