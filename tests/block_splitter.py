


def process_pdf(pdf_path, debug=False):
    steps = [
        OCRStep(dpi=400, lang="por"),
        Cleaner(),
        ExtractRegex(),
    ]

    if debug:
        steps = [
            OCRStep(dpi=400, lang="por"),
            SaveStep(prefix="01_ocr"),
            Cleaner(),
            SaveStep(prefix="02_clean"),
            ExtractRegex(),
            SaveStep(prefix="03_final"),
        ]

    pipeline = ParsePipeline(steps)
    return pipeline.run(pdf_path)


class Cleaner(Step):
    def __init__(self, debug_prefix=None):
        self.debug_prefix = debug_prefix

    def processar(self, texto: str) -> str:
        texto = texto.strip()
        # salva dump se debug estiver ativado
        if self.debug_prefix:
            SaveStep(prefix=self.debug_prefix).processar(texto)
        return texto


steps = [
    OCRStep(dpi=400, lang="por", debug_prefix="01_ocr"),
    Cleaner(debug_prefix="02_clean"),
    ExtractRegex(debug_prefix="03_final"),
]


def with_debug(steps, folder="debug"):
    debugged = []
    for i, step in enumerate(steps, start=1):
        debugged.append(step)
        debugged.append(SaveStep(prefix=f"{i:02d}_{step.__class__.__name__}", folder=folder))
    return debugged


steps = [
    OCRStep(),
    Cleaner(),
    ExtractRegex(),
]

pipeline = ParsePipeline(with_debug(steps))
pipeline.run(pdf_path)


# src/steps/save_step.py (pode ficar junto do SaveStep)

def with_debug(steps, folder="debug"):
    """
    Insere SaveSteps entre cada etapa do pipeline.
    Exemplo:
      [OCRStep(), Cleaner()] ->
      [OCRStep(), SaveStep("01_OCRStep"), Cleaner(), SaveStep("02_Cleaner")]
    """
    debugged = []
    for i, step in enumerate(steps, start=1):
        debugged.append(step)
        debugged.append(SaveStep(prefix=f"{i:02d}_{step.__class__.__name__}", folder=folder))
    return debugged


# src/pipeline/processor_pipeline.py
from src.pipeline.pipeline import ParsePipeline
from src.steps.ocr_step import OCRStep
from src.steps.cleaner import Cleaner
from src.steps.extract_regex import ExtractRegex
from src.steps.save_step import with_debug


def process_pdf(pdf_path, debug=False):
    """
    Executa o pipeline completo em um PDF.
    Se debug=True, injeta SaveSteps após cada etapa.
    """
    steps = [
        OCRStep(dpi=400, lang="por"),
        Cleaner(),
        ExtractRegex(),
    ]

    if debug:
        steps = with_debug(steps, folder="debug")

    pipeline = ParsePipeline(steps)
    return pipeline.run(pdf_path)





