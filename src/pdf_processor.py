import os
import datetime
from src.ocr_utils import pdf_to_text_preprocessed
from src.regex_extractors import extract_fields, extract_codes

def process_pdf(pdf_path):
    folder_name = os.path.basename(os.path.dirname(pdf_path))
    file_name = os.path.basename(pdf_path)
    time_scan = datetime.datetime.fromtimestamp(os.path.getmtime(pdf_path)).isoformat()

    # OCR robusto com pré-processamento, todas as páginas
    # Não salva arquivos intermediários, apenas retorna o texto
    texto_total = pdf_to_text_preprocessed(
        pdf_path,
        save_ocr_path=None,  # Não salva OCR em arquivo
        save_images=False    # Não salva imagens pré-processadas
    )

    # Extrair códigos e campos
    results = []
    matches = extract_codes(texto_total)
    for i, match in enumerate(matches):
        seg_start = match.start()
        seg_end = matches[i + 1].start() if i + 1 < len(matches) else len(texto_total)
        seg = texto_total[seg_start:seg_end]

        codigosrp = match.group(1)
        campos = extract_fields(seg)

        result = {
            "time_scan": time_scan,
            "unidade": folder_name,
            "fileName": file_name,
            "codigosrp": codigosrp,
            **campos
        }
        results.append(result)

    return results
