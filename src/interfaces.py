# src/intefaces.py
from abc import ABC, abstractmethod


class Step(ABC):
    """Classe abstrata que define o contrato das Steps."""

    @abstractmethod
    def processar(self, entrada: str) -> str:
        """Toda etapa deve implementar esse método"""
        pass


# Registry extractors
EXTRACTORS = []
class BaseExtractor(ABC):
    campo = None  # nome do campo, ex: "codigo", "nome"

    def __init_subclass__(cls, **kwargs):
        """
        Toda subclasse registrada automaticamente no Registry
        se definir 'campo'.
        """
        super().__init_subclass__(**kwargs)
        if cls.campo:
            EXTRACTORS.append(cls())  # cria instância e registra

    @abstractmethod
    def extrair(self, texto: str):
        """Todo extractor deve implementar este método"""
        pass


