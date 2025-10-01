# src/parsers/base_normalizers.py
import re
from src.interfaces import BaseNormalizer


class DigitsNormalizer(BaseNormalizer):
    """Normaliza valores pegando só dígitos e validando tamanho."""
    tamanho = None
    minimo = None  # pode ser int ou set de inteiros

    def normalizar(self, valor: str) -> str:
        if not valor:
            return None

        # limpa tudo — mantém só dígitos
        numeros = re.sub(r"\D", "", valor)

        # checa tamanho fixo
        if self.tamanho is not None:
            if len(numeros) != self.tamanho:
                return None
            return numeros

        # checa minimo
        if self.minimo is not None:
            # se for conjunto, valida se comprimento está no conjunto
            if isinstance(self.minimo, set):
                if len(numeros) not in self.minimo:
                    return None
            # se for inteiro, comprimento deve ser >= minimo
            elif isinstance(self.minimo, int):
                if len(numeros) < self.minimo:
                    return None
            else:
                # tipo inválido
                return None

        return numeros



class TextoNormalizer(BaseNormalizer):
    """Normaliza texto comum (nome, profissional, etc.)."""
    permitido = r"[^a-zA-ZçÇ' \-€£¥₩₽]"

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

    def normalizar(self, valor: str) -> str:  # <- self
        if not valor:
            return None
        valor = valor.replace("!", "i")                         
        valor = re.sub(self.permitido, "", valor)       
        valor = re.sub(r"^[A-Za-zçÇ] ", "", valor)
        valor = re.sub(r" [A-Za-zçÇ]$", "", valor)
        valor = re.sub(r" [A-Za-zçÇ] ", " ", valor)
        valor = re.sub(r"\s+", " ", valor).strip()
        return valor or None
