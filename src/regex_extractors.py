import re

# Regex pré-compilados
regex_codigo = re.compile(r"C[oó]digo[:\s]*([0-9]+)", re.I)
regex_nome = re.compile(r"Nome[\s:：;]*([^\n\r]+)", re.I)
regex_exame = [
    re.compile(r"^[ \t]*Exame\s*[:：\.]?\s*([^\n\r]+)", re.I | re.M),
    re.compile(r"^[ \t]*Especialidade\s*[:：\.]?\s*([^\n\r]+)", re.I | re.M),
    re.compile(r"Especialidade\s*[:：\.]?\s*([^\n\r]+?)(?:\s+Tipo Marcação:|\s+Local:|$)", re.I),
    re.compile(r"Exame\s*[:：\.]?\s*([^\n\r]+?)(?:\s+Tipo Marcação:|\s+Local:|$)", re.I),
]
regex_data = [
    re.compile(r"Data Exame[:\s]*([0-3]?\d-\d{2}-\d{4})", re.I),
    re.compile(r"Data Consulta[:\s]*([0-3]?\d-\d{2}-\d{4})", re.I)
]
regex_nasc = re.compile(
    r"Data\s*de\s*Nascimento[:：︓﹕﹔；]?\s*([0-3]?\d[\/.\-:][01]?\d[\/.\-]\d{4})", re.I
)
regex_tel_block = re.compile(r"Telefone:(.*?)(?=Prontu[aá]rio[:\s]|$)", re.I | re.S)
regex_tel = re.compile(r"\(\d{2}\)\s*\d{4,5}-\d{4}")
regex_chegada = re.compile(r"CHEGAR[^\d]*?([0-2]?\d:[0-5]\d)", re.I)
regex_local = re.compile(r"Local[:\s]*(.+)", re.I)

def extract_fields(seg):
    """Extrai todos os campos de um segmento de texto."""
    nome = (regex_nome.search(seg) or ["", ""])[1].strip()

    exameRaw = ""
    for rx in regex_exame:
        m = rx.search(seg)
        if m:
            exameRaw = m.group(1).strip()
            break

    data = ""
    for rx in regex_data:
        m = rx.search(seg)
        if m:
            data = m.group(1).strip()
            break

    nascimento = (regex_nasc.search(seg) or ["", ""])[1].replace(".", "/").replace("-", "/")

    tel_block = (regex_tel_block.search(seg) or ["", ""])[1]
    rawPhones = regex_tel.findall(tel_block)[:4]
    while len(rawPhones) < 4:
        rawPhones.append("")

    chegada = (regex_chegada.search(seg) or ["", ""])[1] if regex_chegada.search(seg) else ""
    local = (regex_local.search(seg) or ["", ""])[1].strip() if regex_local.search(seg) else ""

    return {
        "nome": nome,
        "exameRaw": exameRaw,
        "data": data,
        "nascimento": nascimento,
        "chegada": chegada,
        "local": local,
        "telefones": rawPhones
    }

def extract_codes(texto):
    """Retorna todas as ocorrências de 'Código' no texto."""
    return list(regex_codigo.finditer(texto))
