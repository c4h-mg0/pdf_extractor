# src/pipeline.py
from typing import List
from src.parse_steps.interface import Step


class Pipeline:
    """
    Orquestra a execução sequencial das Steps.
    """

    def __init__(self, Steps: List[Step]):
        self.Steps = Steps

    def run(self, input):
        """
        Executa todas as Steps do pipeline.
        A saída de uma Step é a input da próxima.
        """
        data = input
        for Step in self.Steps:
            data = Step.processar(data)
        return data


