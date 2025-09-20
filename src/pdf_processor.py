# src/processors.py
import os
import datetime
from src.ocr_utils import pdf_to_text_preprocessed
from src.regex_extractors.extract_fields import extract_fields, extract_codes
from src.data_cleaner import normalize_records, deduplicate_records


def get_file_metadata(pdf_path):
    """Coleta nome da pasta, arquivo e timestamp do PDF."""
    folder_name = os.path.basename(os.path.dirname(pdf_path))
    file_name = os.path.basename(pdf_path)
    time_scan = datetime.datetime.fromtimestamp(os.path.getmtime(pdf_path)).isoformat()
    return folder_name, file_name, time_scan


def run_ocr(pdf_path):
    """Executa OCR e retorna texto bruto."""
    ocr_txt_path = pdf_path.replace(".pdf", ".ocr.txt")
    return pdf_to_text_preprocessed(pdf_path, save_ocr_path=ocr_txt_path)


def extract_segments(texto_total):
    """Divide o texto em segmentos com base nos códigos SRP."""
    matches = extract_codes(texto_total)
    for i, match in enumerate(matches):
        seg_start = match.start()
        seg_end = matches[i + 1].start() if i + 1 < len(matches) else len(texto_total)
        yield match.group(1), texto_total[seg_start:seg_end]


def process_pdf(pdf_path):
    """
    Processa um PDF e retorna lista de dicionários:
      1. OCR e extração de campos
      2. Normalização (minúsculo, sem acento, datas/hora unificadas)
      (não remove duplicatas aqui)
    """
    folder_name, file_name, time_scan = get_file_metadata(pdf_path)
    texto_total = run_ocr(pdf_path)

    raw_results = []
    for codigo_srp, segment in extract_segments(texto_total):
        campos = extract_fields(segment)
        result = {
            "time_scan": time_scan,
            "unidade": folder_name,
            "file_name": file_name,
            "codigo_srp": codigo_srp,
            **campos
        }
        raw_results.append(result)

    # Apenas normaliza, sem deduplicar aqui
    normalized = normalize_records(raw_results)
    return normalized

