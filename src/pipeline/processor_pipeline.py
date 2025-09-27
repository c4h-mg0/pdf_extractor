# src/processor/processors.py
from src.ocr.pdf_ocr import PdfOCR
from src.utils.file_utils import save_cleaner
from src.pipeline.stages import Cleaner, ExtractRegex
from src.interfaces import Step

# importa explicitamente para que os extractors se registrem
import src.parsers.extractors
import json




class ParsePipeline:
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



def run_ocr(pdf_path, dpi=400, lang="por"):
    """
    Executa OCR e salva resultado em 'ocr/'.
    Usa a classe PdfOCR.
    """
    ocr_engine = PdfOCR(dpi=dpi, lang=lang)
    texto = ocr_engine.extract(pdf_path)
    ocr_engine.save(texto, pdf_path)
    return texto


def process_pdf(pdf_path):
    texto_total = run_ocr(pdf_path)

    steps = [
        Cleaner(),
        ExtractRegex(),
    ]

    pipeline = ParsePipeline(steps)
    resultado = pipeline.run(texto_total)

    
    texto = json.dumps(resultado, ensure_ascii=False, indent=2)
    save_cleaner(texto, pdf_path)

    
    return resultado

# def process_pdf(pdf_path):
#     texto_total = run_ocr(pdf_path)

#     # Instancia as Steps
#     cleaner = RawCleaner()
#     extractor = ExtractRegex()

#     # ---------- Output do RawCleaner ----------
#     texto_limpo = cleaner.processar(texto_total)
#     with open("raw_cleaner_output.txt", "w", encoding="utf-8") as f:
#         f.write(texto_limpo)

#     # ---------- Pipeline completo ----------
#     steps = [cleaner, extractor]
#     pipeline = Pipeline(steps)
#     resultado = pipeline.run(texto_total)  # mantém o fluxo normal

#     # Salva resultado final (após ExtractRegex)
#     with open("resultado_final.json", "w", encoding="utf-8") as f:
#         f.write(json.dumps(resultado, ensure_ascii=False, indent=2))


#     return resultado


