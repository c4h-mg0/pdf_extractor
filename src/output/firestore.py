import json
import re
from datetime import datetime, timezone, timedelta
from google.cloud import firestore
from google.cloud.firestore_v1.base_query import FieldFilter

# --- Inicializar Firestore (Google Cloud) ---
db = firestore.Client.from_service_account_json("firestore_key.json")


def parse_birthdate(value):
    """Converte string YYYY-MM-DD em string ISO (para Firestore)"""
    if not value:
        return None
    try:
        match = re.match(r"(\d{4}-\d{2}-\d{2})", value)
        if not match:
            return None
        return match.group(1)  # retorna "2019-01-31"
    except Exception:
        return None


def parse_datetime_local_to_utc(value):
    """
    Recebe string no formato ISO (ou compatível) no horário local (UTC-3)
    e converte para datetime UTC universal.
    """
    if not value:
        return None
    try:
        # interpreta como datetime sem fuso
        dt_local = datetime.fromisoformat(value)
        # define que é horário UTC-3
        dt_local = dt_local.replace(tzinfo=timezone(timedelta(hours=-3)))
        # converte para UTC
        dt_utc = dt_local.astimezone(timezone.utc)
        return dt_utc
    except Exception:
        return None
        
def transformar_registro(reg):
    def upper_if_string(v):
        return v.upper() if isinstance(v, str) else v

    return {
        "tipo": upper_if_string(reg.get("tipo")),
        "cross": upper_if_string(reg.get("codigo")),
        "nome": upper_if_string(reg.get("nome")),
        "data_nascimento": parse_birthdate(reg.get("data_nascimento")),  # string ISO, não upper
        "cns": upper_if_string(reg.get("cns")),
        "chegar_as": upper_if_string(reg.get("chegar_as")),
        "agendamento": upper_if_string(reg.get("exame") or reg.get("especialidade")),
        "local": upper_if_string(reg.get("local")),
        "dataAtendimento": parse_datetime_local_to_utc(
            reg.get("data_horario_consulta") or reg.get("data_horario_exame")
        ),
        "unidade": upper_if_string(reg.get("pasta")),
        "data": parse_datetime_local_to_utc(reg.get("arquivo_created_utc"))
    }


def enviar_batch(lista_registros, colecao="nomes"):
    batch = db.batch()
    for reg in lista_registros:
        doc = transformar_registro(reg)
        doc_ref = db.collection(colecao).document()  # ID automático (Firestore padrão)
        batch.set(doc_ref, doc)
        print(f"Preparado: {doc['cross']} -> ID automático")

    batch.commit()
    print(f"✔ {len(lista_registros)} registros enviados ao Firestore em batch.")


if __name__ == "__main__":
    with open("dados.json", "r", encoding="utf-8") as f:
        registros = json.load(f)

    enviar_batch(registros)
