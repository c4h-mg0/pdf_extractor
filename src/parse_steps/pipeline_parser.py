# src/parse_steps/pipeline_parser.py
from src.parse_steps.base_step import Step


class Pipeline:
    """
    Orquestra a execução sequencial das Steps.
    """

    def __init__(self, Steps: list[Step]):
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


