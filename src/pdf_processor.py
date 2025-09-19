# pdf_processor.py
import os
import datetime
from src.ocr_utils import pdf_to_text_preprocessed, save_ocr_text
from src.regex_extractors import extract_fields, extract_codes


def process_pdf(pdf_path):
    folder_name = os.path.basename(os.path.dirname(pdf_path))
    file_name = os.path.basename(pdf_path)
    time_scan = datetime.datetime.fromtimestamp(os.path.getmtime(pdf_path)).isoformat()

    # OCR robusto com pré-processamento, todas as páginas
    ocr_txt_path = pdf_path.replace(".pdf", ".ocr.txt")
    texto_total = pdf_to_text_preprocessed(pdf_path, save_ocr_path=ocr_txt_path)

    # Extrair códigos e campos
    results = []
    matches = extract_codes(texto_total)
    for i, match in enumerate(matches):
        seg_start = match.start()
        seg_end = matches[i + 1].start() if i + 1 < len(matches) else len(texto_total)
        seg = texto_total[seg_start:seg_end]

        codigosrp = match.group(1)
        campos = extract_fields(seg)  # agora já inclui cns, hora_atendimento e profissional

        result = {
            "time_scan": time_scan,
            "unidade": folder_name,
            "fileName": file_name,
            "codigosrp": codigosrp,
            **campos  # inclui nome, especialidade/exame, dataAtendimento, nascimento,
                      # horachegada, local, telefone, cns, hora_atendimento, profissional (se existir)
        }
        results.append(result)

    return results
