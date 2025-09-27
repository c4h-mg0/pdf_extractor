# src/parse_steps/pipeline_parser.py
from src.interfaces import Step
from src.parsers.cleaners import *
from src.interfaces import EXTRACTORS
import re


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


class ExtractRegex(Step):
    def processar(self, texto: str) -> list:  
        # Divide o texto por cada ocorrência de "codigo:" (cada página/paciente)
        blocos = re.split(r"(?=codigo:)", texto)
        blocos = [b.strip() for b in blocos if b.strip()]

        resultado_total = []

        for bloco in blocos:
            dados = {}
            for extractor in EXTRACTORS:
                valor = extractor.extrair(bloco)
                dados[extractor.campo] = valor
            resultado_total.append(dados)

        return resultado_total