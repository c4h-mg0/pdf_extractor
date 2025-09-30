# src/pipeline/processor_pipeline.py
from src.pipeline.stages import RunOcr, Cleaner, ExtractRegex, NormalizerRegex, SaveStep
from src.interfaces import Step

# importa explicitamente para que os extractors se registrem
import src.parsers.extractors
import src.parsers.normalizers

class StagePipeline:
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


def process_pdf(pdf_path):
    steps = [
        RunOcr(),
        Cleaner(),
        ExtractRegex(),
        NormalizerRegex(),
    ]
    pipeline = StagePipeline(with_debug(steps))
    resultado = pipeline.run(pdf_path)
    return resultado

    
def with_debug(steps, folder="debug"):
    debugged = []
    for i, step in enumerate(steps, start=1):
        debugged.append(step)
        debugged.append(SaveStep(prefix=f"{i:02d}_{step.__class__.__name__}", folder=folder))
    return debugged




