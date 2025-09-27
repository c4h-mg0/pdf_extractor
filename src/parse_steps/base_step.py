# src/parse_steps/base_step.py
from abc import ABC, abstractmethod


class Step(ABC):
    """Classe abstrata que define o contrato das Steps."""

    @abstractmethod
    def processar(self, entrada: str) -> str:
        """Toda etapa deve implementar esse método"""
        pass

       



