# patterns.py

import re

# ---------------------------
# Código SRP
# ---------------------------
REGEX_CODIGO = re.compile(r"C[oó]digo[:\s]*([0-9]+)", re.I)

# ---------------------------
# Nome
# ---------------------------
REGEX_NOME = re.compile(r"Nome[\s:：;]*([^\n\r]+)", re.I)

# ---------------------------
# Exame / Especialidade
# ---------------------------
REGEX_EXAME = [
    (re.compile(r"^[ \t]*Exame\s*[:：\.]?\s*([^\n\r]+)", re.I | re.M), "exame"),
    (re.compile(r"^[ \t]*Especialidade\s*[:：\.]?\s*([^\n\r]+)", re.I | re.M), "especialidade"),
    (re.compile(r"Especialidade\s*[:：\.]?\s*([^\n\r]+?)(?:\s+Tipo Marcação:|\s+Local:|$)", re.I), "especialidade"),
    (re.compile(r"Exame\s*[:：\.]?\s*([^\n\r]+?)(?:\s+Tipo Marcação:|\s+Local:|$)", re.I), "exame"),
]

# ---------------------------
# Datas / Horários
# ---------------------------
REGEX_DATA = [
    (re.compile(r"Data Exame[:\s]*([0-3]?\d-\d{2}-\d{4})", re.I), "data_exame"),
    (re.compile(r"Data Consulta[:\s]*([0-3]?\d-\d{2}-\d{4})", re.I), "data_consulta")
]
REGEX_HORA = re.compile(r"Hor[áa]rio[:\s]*([0-2]?\d:[0-5]\d)", re.I)

# ---------------------------
# Nascimento
# ---------------------------
REGEX_NASC = re.compile(
    r"Data\s*de\s*Nascimento[:：︓﹕﹔；]?\s*([0-3]?\d[\/.\-:][01]?\d[\/.\-]\d{4})", re.I
)

# ---------------------------
# Telefones
# ---------------------------
REGEX_TEL_BLOCK = re.compile(r"Telefone:(.*?)(?=Prontu[aá]rio[:\s]|$)", re.I | re.S)
REGEX_TEL = re.compile(r"\(\d{2}\)\s*\d{4,5}-\d{4}")

# ---------------------------
# Local
# ---------------------------
REGEX_LOCAL = re.compile(r"Local[:\s]*(.+)", re.I)

# ---------------------------
# CNS
# ---------------------------
REGEX_CNS = re.compile(r"Cns[:\s]*([\d,\s]+)", re.I)

# ---------------------------
# Profissional
# ---------------------------
REGEX_PROFISSIONAL = re.compile(r"Profissional[:\s]*([^\n\r]+)", re.I)

# ---------------------------
# Horário chegada
# ---------------------------
REGEX_CHEGADA = re.compile(r"CHEGAR[^\d]*?([0-2]?\d:[0-5]\d)", re.I)



