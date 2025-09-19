import re

# Regex pré-compilados existentes
regex_codigo = re.compile(r"C[oó]digo[:\s]*([0-9]+)", re.I)
regex_nome = re.compile(r"Nome[\s:：;]*([^\n\r]+)", re.I)
regex_exame = [
    (re.compile(r"^[ \t]*Exame\s*[:：\.]?\s*([^\n\r]+)", re.I | re.M), "exame"),
    (re.compile(r"^[ \t]*Especialidade\s*[:：\.]?\s*([^\n\r]+)", re.I | re.M), "especialidade"),
    (re.compile(r"Especialidade\s*[:：\.]?\s*([^\n\r]+?)(?:\s+Tipo Marcação:|\s+Local:|$)", re.I), "especialidade"),
    (re.compile(r"Exame\s*[:：\.]?\s*([^\n\r]+?)(?:\s+Tipo Marcação:|\s+Local:|$)", re.I), "exame"),
]
regex_data = [
    (re.compile(r"Data Exame[:\s]*([0-3]?\d-\d{2}-\d{4})", re.I), "data_exame"),
    (re.compile(r"Data Consulta[:\s]*([0-3]?\d-\d{2}-\d{4})", re.I), "data_consulta")
]
regex_nasc = re.compile(
    r"Data\s*de\s*Nascimento[:：︓﹕﹔；]?\s*([0-3]?\d[\/.\-:][01]?\d[\/.\-]\d{4})", re.I
)
regex_tel_block = re.compile(r"Telefone:(.*?)(?=Prontu[aá]rio[:\s]|$)", re.I | re.S)
regex_tel = re.compile(r"\(\d{2}\)\s*\d{4,5}-\d{4}")
regex_chegada = re.compile(r"CHEGAR[^\d]*?([0-2]?\d:[0-5]\d)", re.I)
regex_local = re.compile(r"Local[:\s]*(.+)", re.I)

# Novos regex
regex_cns = re.compile(r"Cns[:\s]*([\d,\s]+)", re.I)

regex_hora_atend = [
    (re.compile(r"Hor[áa]rio[:\s]*([0-2]?\d:[0-5]\d)", re.I), "hora_exame"),    # vamos ajustar depois pelo tipo
]

regex_profissional = re.compile(r"Profissional[:\s]*([^\n\r]+)", re.I)


def extract_fields(seg):
    nome = (regex_nome.search(seg) or ["", ""])[1].strip()

    # Captura exame/especialidade
    exameRaw = ""
    exame_tipo = "exameRaw"
    for rx, tipo in regex_exame:
        m = rx.search(seg)
        if m:
            exameRaw = m.group(1).strip()
            exame_tipo = tipo
            break

    # --------- Ajuste para data + hora dinâmica ---------
    data_key = ""
    data_val = ""
    for rx, key in regex_data:
        m = rx.search(seg)
        if m:
            data_val = m.group(1).strip()
            data_key = key
            break

    # Captura hora ligada ao tipo de data encontrado
    hora_val = ""
    hora_key = ""
    if data_key:  # só tenta achar hora se encontrou data
        m_hora = re.search(r"Hor[áa]rio[:\s]*([0-2]?\d:[0-5]\d)", seg, re.I)
        if m_hora:
            hora_val = m_hora.group(1)
            hora_key = data_key.replace("data", "hora")  # transforma data_exame -> hora_exame

    # ----------------- Demais campos -------------------
    nascimento = (regex_nasc.search(seg) or ["", ""])[1].replace(".", "/").replace("-", "/")

    tel_block = (regex_tel_block.search(seg) or ["", ""])[1]
    rawPhones = regex_tel.findall(tel_block)[:4]
    while len(rawPhones) < 4:
        rawPhones.append("")
    telefones_str = " ".join([f"+55{re.sub(r'[^0-9]', '', t)}" for t in rawPhones if t])

    chegar_as = (regex_chegada.search(seg) or ["", ""])[1] if regex_chegada.search(seg) else ""
    local = (regex_local.search(seg) or ["", ""])[1].strip() if regex_local.search(seg) else ""

    # Novos campos extras
    cns = ""
    m_cns = regex_cns.search(seg)
    if m_cns:
        cns = " ".join(re.split(r"[,\s]+", m_cns.group(1).strip()))

    profissional = ""
    m_prof = regex_profissional.search(seg)
    if m_prof:
        profissional = m_prof.group(1).strip()

    # ---------- Monta dicionário dinâmico ----------
    result = {
        "nome": nome,
        exame_tipo: exameRaw,
        "nascimento": nascimento,
        "chegar_as": chegar_as,
        "local": local,
        "telefone": telefones_str
    }

    # Adiciona data/hora com chave dinâmica
    if data_key:
        result[data_key] = data_val
    if hora_key:
        result[hora_key] = hora_val

    # Adiciona extras se existirem
    if cns:
        result["cns"] = cns
    if profissional:
        result["profissional"] = profissional

    return result


def extract_codes(texto):
    """Retorna todas as ocorrências de 'Código' no texto."""
    return list(regex_codigo.finditer(texto))
