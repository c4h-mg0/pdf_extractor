# src/intefaces.py
from abc import ABC, abstractmethod


class Step(ABC):
    """Classe abstrata que define o contrato das Steps."""

    @abstractmethod
    def processar(self, entrada: str) -> str:
        """Toda etapa deve implementar esse método"""
        pass


class BaseExtractor(ABC):
    """Base para todos os extractors (regex, etc.)."""
    campo = None
    tipos = ["consulta", "exame"]
    registry = []  # todos extractors registrados

    def __init_subclass__(cls, **kwargs):
        """
        Toda subclasse registrada automaticamente no registry
        se definir 'campo'.
        """
        super().__init_subclass__(**kwargs)
        if cls.campo:
            BaseExtractor.registry.append(cls())  # cria instância e registra

    @abstractmethod
    def extrair(self, texto: str):
        """Todo extractor deve implementar este método"""
        pass

