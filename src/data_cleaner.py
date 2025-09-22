# src/data_cleaner.py
import unicodedata
from datetime import datetime
import os
import re
from typing import Union, List, Dict

def remove_spaces_numeric_like(record: dict) -> dict:
    """
    Remove espaços apenas de campos que parecem datas, horas ou códigos curtos.
    - Datas e horas: contêm apenas números e símbolos, ou nome sugere data/hora
    - Códigos curtos (menos de 15 caracteres): juntar números
    - Valores longos (ex: CNS) não são tocados
    """
    campos_alvo_substrings = ["data", "hora", "codigo", "chegar_as", "nascimento",]
    novo = {}
    
    for k, v in record.items():
        if not isinstance(v, str):
            novo[k] = v
            continue
        
        # remove espaços em datas/horas ou campos que sugerem isso
        if any(sub in k.lower() for sub in campos_alvo_substrings):
            novo[k] = v.replace(" ", "")
        # remove espaços em valores numeric-like curtos (códigos)
        elif all(c.isdigit() or c in "-/: " for c in v) and len(v) <= 14:
            novo[k] = v.replace(" ", "")
        else:
            # tudo mais mantém (CNS, nomes, etc.)
            novo[k] = v
            
    return novo


def clean_fields(data: Union[Dict, List[Dict]]) -> Union[Dict, List[Dict]]:
    """
    Limpa prefixos e sujidades finais (; : . - |) de todos os valores string
    de um dicionário ou de uma lista de dicionários.
    """
    def _clean_value(v: str) -> str:
        if not v:
            return ""
        v = v.strip()
        v = re.sub(r"^[\s:;,\-\.\|]+", "", v)   # remove prefixo sujo
        v = re.sub(r"[\s:;,\-\.\|]+$", "", v)   # remove sujidade final
        return v

    def _clean_dict(d: Dict) -> Dict:
        return {
            k: _clean_value(v) if isinstance(v, str) else v
            for k, v in d.items()
        }

    if isinstance(data, dict):
        return _clean_dict(data)
    elif isinstance(data, list):
        return [_clean_dict(d) for d in data]
    else:
        raise TypeError("clean_fields aceita apenas dict ou lista de dicts")


def clean_date_str(date_str: str) -> str:
    """Padroniza separadores de data para '-'."""
    if not date_str:
        return ""
    date_str = date_str.strip()
    # troca / ou . por -
    date_str = re.sub(r"[\/.]", "-", date_str)
    return date_str


def remove_accents(text: str) -> str:
    """Remove acentos de uma string."""
    if not isinstance(text, str):
        return text
    nfkd = unicodedata.normalize("NFKD", text)
    return "".join([c for c in nfkd if not unicodedata.combining(c)])


# Pega timestamps no formato YYYY-MM-DDTHH:MM:SS
ISO_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$")

def to_lowercase(record: dict) -> dict:
    """
    Converte strings para minúsculo, exceto quando
    a string está em formato de timestamp ISO8601.
    """
    def maybe_lower(val):
        if isinstance(val, str):
            # Não altera timestamps ISO8601
            if ISO_PATTERN.match(val):
                return val
            return val.lower()
        return val

    return {k: maybe_lower(v) for k, v in record.items()}


def unify_datetime_fields(record: dict) -> dict:
    """
    Une data_exame+hora_exame e data_consulta+hora_consulta em timestamps.
    Converte também nascimento e chegar_as para timestamps.
    """
    def parse_timestamp(date_str, time_str=None):
        if not date_str:
            return None
        try:
            date_str = clean_date_str(date_str)
            full_str = date_str if not time_str else f"{date_str} {time_str}"
            fmt = "%d-%m-%Y" if not time_str else "%d-%m-%Y %H:%M"
            return datetime.strptime(full_str, fmt).isoformat()
        except Exception:
            return None

    # Exame
    if "data_exame" in record:
        record["data_hora_exame"] = parse_timestamp(record.get("data_exame"), record.get("hora_exame"))
        record.pop("data_exame", None)
        record.pop("hora_exame", None)

    # Consulta
    if "data_consulta" in record:
        record["data_hora_consulta"] = parse_timestamp(record.get("data_consulta"), record.get("hora_consulta"))
        record.pop("data_consulta", None)
        record.pop("hora_consulta", None)

    # Nascimento
    if "nascimento" in record:
        record["nascimento"] = parse_timestamp(record.get("nascimento"))

    # Chegar_as
    if "chegar_as" in record:
        # Aqui precisamos de uma data base pra criar timestamp, senão fica só hora
        record["chegar_as"] = parse_timestamp(datetime.now().strftime("%d-%m-%Y"), record.get("chegar_as"))

    return record


def normalize_records(records: list) -> list:
    """Pipeline completo: minúsculo, sem acento, datas unificadas, sem duplicata."""
    normalized = []
    for r in records:
        r = remove_spaces_numeric_like(r)
        r = {k: remove_accents(v) if isinstance(v, str) else v for k, v in r.items()}
        r = unify_datetime_fields(r)
        r = to_lowercase(r)
        r = clean_fields(r)
        normalized.append(r)
    return normalized


def deduplicate_records(records: list, log_path="fix.txt", stats: dict = None) -> list:
    """
    Deduplica registros:
      - Remove duplicatas com base em codigo_srp + exame/especialidade (ou fallback).
      - Mantém o mais recente.
    Logging:
      - === RESUMO POR PASTA ===: nº de PDFs e nº de documentos extraídos por pasta.
      - === DUPLICADOS REMOVIDOS ===: registros descartados por duplicidade.
      - === CAMPOS VAZIOS (NÃO REMOVIDOS) ===: registros com algum campo "".
    """

    def build_key(r):
        codigo = r.get("codigo_srp") or r.get("nome") or ""
        exame_espec = r.get("exame") or r.get("especialidade")
        if not exame_espec:
            exame_espec = f"{r.get('local','')}|{r.get('data_hora_exame','')}|{r.get('data_hora_consulta','')}"
        return f"{codigo}|{exame_espec}"

    def parse_time(t):
        try:
            return datetime.fromisoformat(t)
        except Exception:
            return datetime.min

    best_records = {}
    duplicados = []
    com_vazios = []

    for r in records:
        key = build_key(r)
        current_time = parse_time(r.get("time_scan", ""))

        if key not in best_records:
            best_records[key] = r
        else:
            existing = best_records[key]
            existing_time = parse_time(existing.get("time_scan", ""))

            if current_time > existing_time:
                duplicados.append(existing)
                best_records[key] = r
            else:
                duplicados.append(r)

    # Detecta registros com campos vazios (mas não remove)
    for r in best_records.values():
        if any(v == "" for v in r.values()):
            com_vazios.append(r)

    # Escreve o log
    with open(log_path, "w", encoding="utf-8") as f:
        # Resumo
        if stats:
            f.write("=== RESUMO POR PASTA ===\n")
            for pasta, dados in stats.items():
                f.write(f"{pasta}: {dados['pdfs']} arquivos PDF, {dados['docs']} documentos extraídos\n")
            f.write("\n")

        # Duplicados
        f.write(f"=== DUPLICADOS REMOVIDOS (total: {len(duplicados)}) ===\n")
        if duplicados:
            for r in duplicados:
                f.write(str(r) + "\n")
        else:
            f.write("(nenhum)\n")
        f.write("\n")

        # Vazios
        f.write(f"=== CAMPOS VAZIOS (NÃO REMOVIDOS) (total: {len(com_vazios)}) ===\n")
        if com_vazios:
            for r in com_vazios:
                f.write(str(r) + "\n")
        else:
            f.write("(nenhum)\n")

    return list(best_records.values())
