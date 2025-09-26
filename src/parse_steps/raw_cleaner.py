# src/parser_steps/cleaner.py
import re
import unicodedata
from src.parse_steps.interface import Step


class RawCleaner(Step):
    """
    Etapa de limpeza global do texto OCR:
    - Remove caracteres invisíveis
    - Normaliza acentos
    - Padroniza separadores em chave:valor
    - Remove espaços desnecessários
    """

    def _remover_invisiveis(self, texto: str) -> str:
        """Remove caracteres de controle não imprimíveis"""
        return "".join(ch for ch in texto if ch.isprintable())

    def _remover_acentos(self, texto: str) -> str:
        """Remove acentos mantendo apenas letras ASCII"""
        nfkd = unicodedata.normalize("NFKD", texto)
        return "".join(c for c in nfkd if not unicodedata.combining(c))

    def _normalizar_separadores(self, texto: str) -> str:
        """
        Troca separadores estranhos (.;,) por ":" apenas em contextos chave:valor.
        Exemplo: 'Codigo; 123' -> 'Codigo:123'
        """
        return re.sub(r"\s*[:;.,]\s*", ":", texto)

    def _ajustar_espacos(self, texto: str) -> str:
        """Remove espaços repetidos e antes/depois de pontuação"""
        texto = re.sub(r"\s+([:/\-])", r"\1", texto)  # espaço antes de : / -
        texto = re.sub(r"([:/\-])\s+", r"\1", texto)  # espaço depois de : / -
        texto = re.sub(r"\s+", " ", texto)            # múltiplos espaços -> um
        return texto.strip()

    def processar(self, entrada: str) -> str:
        """Aplica todas as limpezas em ordem"""
        texto = self._remover_invisiveis(entrada)
        texto = self._remover_acentos(texto)
        texto = self._normalizar_separadores(texto)
        texto = self._ajustar_espacos(texto)
        return texto
