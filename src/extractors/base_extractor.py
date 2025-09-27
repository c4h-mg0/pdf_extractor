# src/extractor/base_extractor.py
from abc import ABC, abstractmethod

# Registry global
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
