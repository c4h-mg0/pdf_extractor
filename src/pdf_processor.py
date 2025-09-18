import os
import datetime
from src.ocr_utils import pdf_to_text
from src.regex_extractors import extract_fields, extract_codes


def process_pdf(pdf_path):
    folder_name = os.path.basename(os.path.dirname(pdf_path))
    file_name = os.path.basename(pdf_path)

    # time_scan = data de modificação do arquivo (não o horário do script!)
    time_scan = datetime.datetime.fromtimestamp(os.path.getmtime(pdf_path)).isoformat()

    texto_total = pdf_to_text(pdf_path, lang="por")
    matches = extract_codes(texto_total)

    results = []
    for i, match in enumerate(matches):
        seg_start = match.start()
        seg_end = matches[i + 1].start() if i + 1 < len(matches) else len(texto_total)
        seg = texto_total[seg_start:seg_end]

        codigosrp = match.group(1)  # código SRP do paciente
        campos = extract_fields(seg)  # retorna dict com nome, telefone, exame/especialidade etc.

        # Monta resultado final
        result = {
            "time_scan": time_scan,
            "unidade": folder_name,
            "fileName": file_name,
            "codigosrp": codigosrp,
            **campos  # inclui nome, exame/especialidade, dataAtendimento, nascimento, horachegada, local, telefone
        }

        results.append(result)

    return results
