# src/processor/processors.py
from src.pipeline.stages import RunOcr, Cleaner, ExtractRegex, with_debug
from src.interfaces import Step



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


def process_pdf(pdf_path):
    
    steps = [
        RunOcr(),
        Cleaner(),
        ExtractRegex(),
    ]

    # pipeline = ParsePipeline(steps)

    pipeline = ParsePipeline(with_debug(steps, base_folder="debug"))
    resultado = pipeline.run(pdf_path)


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


