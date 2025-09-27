# src/parser_steps/raw_cleaner.py
import re
import unicodedata
from src.parse_steps.base_step import Step


class RawCleaner(Step):
    """
    Etapa de limpeza global do texto OCR:
    - Remove caracteres invisíveis
    - Normaliza acentos
    - Padroniza separadores em chave:valor
    - Remove espaços desnecessários
    """

    def _remover_invisiveis(self, texto: str) -> str:
        """Remove caracteres de controle não imprimíveis, preservando \n"""
        return "".join(ch for ch in texto if ch.isprintable() or ch == "\n")

    def _remover_acentos(self, texto: str) -> str:
        """Remove acentos mantendo apenas letras ASCII"""
        nfkd = unicodedata.normalize("NFKD", texto)
        return "".join(c for c in nfkd if not unicodedata.combining(c))

    def _ajustar_espacos(self, texto: str) -> str:
        """Remove espaços repetidos e antes/depois de pontuação sem matar \n"""
        texto = re.sub(r"[ \t]+([:/\-])", r"\1", texto)   # espaço antes de : / -
        texto = re.sub(r"[ \t]{2,}", " ", texto)          # múltiplos espaços -> um
        return "\n".join(line.strip() for line in texto.splitlines())

    def _texto_lower(self, texto: str) -> str:
        return texto.lower()

    def processar(self, entrada: str) -> str:
        """Aplica todas as limpezas em ordem"""
        texto = self._remover_invisiveis(entrada)
        texto = self._remover_acentos(texto)
        texto = self._texto_lower(texto)
        texto = self._ajustar_espacos(texto)
        return texto
