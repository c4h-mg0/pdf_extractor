import json
import firebase_admin
from firebase_admin import credentials, firestore

# --- Inicializar Firestore ---
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def transformar_registro(reg):
    """Aplica as regras de transformação"""
    return {
        "tipo": reg.get("tipo"),
        "cross": reg.get("codigo"),
        "nome": reg.get("nome"),
        "data_nascimento": reg.get("data_nascimento"),
        "cns": reg.get("cns"),
        "chegar_as": reg.get("chegar_as"),
        "agendamento": reg.get("exame") or reg.get("especialidade"),
        "local": reg.get("local"),
        "dataAtendimento": reg.get("data_horario_consulta") or reg.get("data_horario_exame"),
        "unidade": reg.get("pasta"),
        "data": reg.get("arquivo_created_utc")
    }

def enviar_batch(lista_registros, colecao="atendimentos"):
    batch = db.batch()
    for reg in lista_registros:
        doc = transformar_registro(reg)
        doc_ref = db.collection(colecao).document(doc["cross"])
        batch.set(doc_ref, doc)
        print(f"Preparado: {doc['cross']}")

    batch.commit()
    print(f"✔ {len(lista_registros)} registros enviados ao Firestore em batch.")

if __name__ == "__main__":
    with open("dados.json", "r", encoding="utf-8") as f:
        registros = json.load(f)

    enviar_batch(registros)
