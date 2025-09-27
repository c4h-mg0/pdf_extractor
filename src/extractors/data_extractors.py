# src/extractor/data_extractors.py
import re
from src.extractors.base_extractor import BaseExtractor


class CodigoExtractor(BaseExtractor):
    campo = "codigo"

    def extrair(self, texto: str):
        match = re.search(r"codigo:\s*(\d+)", texto, re.IGNORECASE)
        return match.group(1) if match else None


class NomeExtractor(BaseExtractor):
    campo = "nome"

    def extrair(self, texto: str):
        match = re.search(r"nome:\s*([a-z\s]+)", texto, re.IGNORECASE)
        return match.group(1).strip() if match else None
