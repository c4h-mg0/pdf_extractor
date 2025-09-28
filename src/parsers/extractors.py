# src/parsers/extractors.py
import re
from src.interfaces import BaseExtractor


class CodigoExtractor(BaseExtractor):
    campo = "codigo"

    def extrair(self, texto: str):
        regex = r"c[o0]digo\s*[:;.,-]?\s*([\d\s.,]{3,12})"
        match = re.search(regex, texto)
        return match.group(1).splitlines()[0].strip() if match else None


class NomeExtractor(BaseExtractor):
    campo = "nome"

    def extrair(self, texto: str):
        match = re.search(r"(?:nome|neme)\s*[:;.,]?\s*([a-z '!\-]+)", texto)
        return match.group(1).strip().split("\n")[0] if match else None
