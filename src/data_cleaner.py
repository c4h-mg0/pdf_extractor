# src/data_cleaner.py
import unicodedata
from datetime import datetime
import os
import re


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

def to_lowercase(record: dict) -> dict:
    """Converte todas as strings para minúsculo."""
    return {k: v.lower() if isinstance(v, str) else v for k, v in record.items()}


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
        r = to_lowercase(r)
        r = {k: remove_accents(v) if isinstance(v, str) else v for k, v in r.items()}
        r = unify_datetime_fields(r)
        normalized.append(r)
    return normalized



def deduplicate_records(records: list, log_path="fix.txt") -> list:
    """
    Remove duplicatas com base nas regras definidas:
    - codigo_srp + exame/especialidade
    - fallback para nome ou local/data/hora se necessário
    Mantém o registro com timestamp mais recente.
    Salva log dos removidos com campos em branco.
    """

    def build_key(r):
        """Cria chave para comparação, com fallback."""
        codigo = r.get("codigo_srp") or r.get("nome") or ""
        exame_espec = r.get("exame") or r.get("especialidade")
        if not exame_espec:
            exame_espec = f"{r.get('local','')}|{r.get('data_hora_exame','')}|{r.get('data_hora_consulta','')}"
        return f"{codigo}|{exame_espec}"

    def parse_time(t):
        """Converte timestamp para datetime para comparação."""
        try:
            return datetime.fromisoformat(t)
        except Exception:
            return datetime.min

    # Dicionário para manter o melhor registro
    best_records = {}
    removed = []

    for r in records:
        key = build_key(r)
        current_time = parse_time(r.get("time_scan", ""))

        if key not in best_records:
            best_records[key] = r
        else:
            existing = best_records[key]
            existing_time = parse_time(existing.get("time_scan", ""))

            # Mantém o mais recente
            if current_time > existing_time:
                removed.append(existing)
                best_records[key] = r
            else:
                removed.append(r)

    # Log dos removidos com campos em branco
    if removed:
        with open(log_path, "w", encoding="utf-8") as f:
            for r in removed:
                if any(v == "" for v in r.values()):
                    f.write(str(r) + "\n")

    return list(best_records.values())
