# src/parse_steps/extract_regex.py
import re
from src.parse_steps.base_step import Step
from src.extractors.base_extractor import EXTRACTORS

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



