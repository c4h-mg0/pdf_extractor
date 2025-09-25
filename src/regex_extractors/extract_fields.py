import re
from src.regex_extractors import patterns


def extract_nome(seg: str) -> dict:
    m = patterns.REGEX_NOME.search(seg)
    return {"nome": m.group(1).strip()} if m else {"nome": ""}


def extract_exame(seg: str) -> dict:
    for rx, tipo in patterns.REGEX_EXAME:
        m = rx.search(seg)
        if m:
            return {tipo: m.group(1).strip()}
    return {"exame": ""}


def extract_datas(seg: str) -> dict:
    result = {}
    for rx, key in patterns.REGEX_DATA:
        m = rx.search(seg)
        if m:
            result[key] = m.group(1).strip()
            # tenta capturar hora relacionada
            m_hora = patterns.REGEX_HORA.search(seg)
            if m_hora:
                result[key.replace("data", "hora")] = m_hora.group(1)
            break
    return result


def extract_telefones(seg: str) -> dict:
    tel_block = (patterns.REGEX_TEL_BLOCK.search(seg) or ["", ""])[1]
    rawPhones = patterns.REGEX_TEL.findall(tel_block)[:4]
    while len(rawPhones) < 4:
        rawPhones.append("")
    telefones_str = " ".join([f"+55{re.sub(r'[^0-9]', '', t)}" for t in rawPhones if t])
    return {"telefone": telefones_str}


def extract_local(seg: str) -> dict:
    m = patterns.REGEX_LOCAL.search(seg)
    return {"local": m.group(1).strip()} if m else {"local": ""}


def extract_profissional(seg: str) -> dict:
    m = patterns.REGEX_PROFISSIONAL.search(seg)
    return {"profissional": m.group(1).strip()} if m else {"profissional": ""}


def extract_cns(seg: str) -> dict:
    m = patterns.REGEX_CNS.search(seg)
    if not m:
        return {}
    raw_parts = re.split(r"[,\s]+", m.group(1).strip())
    digits = "".join(raw_parts)
    cns_list = [digits[i:i+15] for i in range(0, len(digits), 15)]
    return {"cns": " ".join(cns_list)}


def extract_nascimento(seg: str) -> dict:
    m = patterns.REGEX_NASC.search(seg)
    if not m:
        return {"nascimento": ""}
    nasc = m.group(1).replace(".", "/").replace("-", "/")
    return {"nascimento": nasc}


def extract_chegada(seg: str) -> dict:
    m = patterns.REGEX_CHEGADA.search(seg)
    return {"chegar_as": m.group(1)} if m else {"chegar_as": ""}


# ----------------------------------------------------------------
# Extrai o código srp único, delimitando a quantidade de registros
# ----------------------------------------------------------------
def extract_codes(texto: str):
    return list(patterns.REGEX_CODIGO.finditer(texto))

# ---------------------------
# Orquestrador
# ---------------------------
def extract_fields(seg: str) -> dict:
    result = {}
    for extractor in [
        extract_nome,
        extract_exame,
        extract_datas,
        extract_nascimento,
        extract_telefones,
        extract_local,
        extract_profissional,
        extract_cns,
        extract_chegada,
    ]:
        result.update(extractor(seg))
    return result

