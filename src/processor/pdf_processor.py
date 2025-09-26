# src/processors.py
from src.ocr.pdf_ocr import PdfOCR
from src.utils.file_utils import save_cleaner
from src.parse_steps.raw_cleaner import RawCleaner
from src.parse_steps.bock_splitter import BlockSplitter
from src.parse_steps.pipeline_parser import Pipeline


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
        RawCleaner(),
        BlockSplitter(),
    ]

    pipeline = Pipeline(steps)
    resultado = pipeline.run(texto_total)   # resultado é list[str]

    # Concatena os blocos em um único texto para salvar
    texto_formatado = "\n\n".join(
        [f"===== BLOCO {i+1} =====\n{bloco}" for i, bloco in enumerate(resultado)]
    )

    # Agora sim salva no txt
    save_cleaner(texto_formatado, pdf_path, folder="ocr_clean")

    # Retorna os blocos como lista (para uso posterior no código)
    return resultado
    
