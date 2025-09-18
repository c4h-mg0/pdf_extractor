import os
import datetime
from src.ocr_utils import pdf_to_text
from src.regex_extractors import extract_fields, extract_codes

def process_pdf(pdf_path, cfg_nome="CFG_DEFAULT"):
    folder_name = os.path.basename(os.path.dirname(pdf_path))
    file_name = os.path.basename(pdf_path)

    # timestamp = data de modificação do arquivo (não o horário do script!)
    timestamp = datetime.datetime.fromtimestamp(os.path.getmtime(pdf_path)).isoformat()

    texto_total = pdf_to_text(pdf_path, lang="por")
    matches = extract_codes(texto_total)

    results = []
    for i, match in enumerate(matches):
        seg_start = match.start()
        seg_end = matches[i + 1].start() if i + 1 < len(matches) else len(texto_total)
        seg = texto_total[seg_start:seg_end]

        codigoVal = match.group(1)
        campos = extract_fields(seg)

        results.append({
            "timestamp": timestamp,
            "pasta": folder_name,
            "fileName": file_name,
            "codigoVal": codigoVal,
            "cfg_nome": cfg_nome,
            "nome": campos["nome"],
            "exameRaw": campos["exameRaw"],
            "data": campos["data"],
            "nascimento": campos["nascimento"],
            "chegada": campos["chegada"],
            "local": campos["local"],
            "telefone1": campos["telefones"][0],
            "telefone2": campos["telefones"][1],
            "telefone3": campos["telefones"][2],
            "telefone4": campos["telefones"][3],
        })

    return results
