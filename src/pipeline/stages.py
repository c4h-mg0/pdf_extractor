# src/parse_steps/pipeline_parser.py
from src.ocr.pdf_ocr import PdfOCR
from src.interfaces import Step, BaseExtractor
from src.parsers.cleaners import *
import re


class RunOcr(Step):
    def __init__(self, dpi=400, lang="por"):
        self.dpi = dpi
        self.lang = lang

    def processar(self, pdf_path: str) -> str:
        """
        Executa OCR e retorna o texto.
        """
        ocr_engine = PdfOCR(dpi=self.dpi, lang=self.lang)
        texto = ocr_engine.extract(pdf_path)
        ocr_engine.save(texto, pdf_path)
        return texto


class Cleaner(Step):     
    """
    Aplica todas as limpezas em ordem
    Etapa de limpeza global do texto OCR:
    - Remove caracteres invisíveis
    - Normaliza acentos
    - Padroniza separadores em chave:valor
    - Remove espaços desnecessários
    """
    def processar(self, entrada: str) -> str:
        texto = remover_invisiveis(entrada)
        texto = remover_acentos(texto)
        texto = texto_lower(texto)
        texto = ajustar_espacos(texto)
        return texto


class SplitBlocks(Step):
    def processar(self, texto: str) -> list[str]:
        """
        Divide o texto em blocos de pacientes/páginas.
        Ordem de fallback:
        1. codigo:
        2. local:
        3. quebra dupla de linha
        """
        # 1. Tenta com "codigo:"
        blocos = re.split(r"(?=codigo:)", texto)
        blocos = [b.strip() for b in blocos if b.strip()]

        # 2. Fallback: usa "local:"
        if not blocos or len(blocos) == 1:
            blocos = re.split(r"(?=local:)", texto)
            blocos = [b.strip() for b in blocos if b.strip()]

        # 3. Fallback final: divide por linha em branco
        if not blocos or len(blocos) == 1:
            blocos = re.split(r"\n\s*\n", texto)
            blocos = [b.strip() for b in blocos if b.strip()]

        return blocos


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



