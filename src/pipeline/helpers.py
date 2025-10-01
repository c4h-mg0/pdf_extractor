import os
import json
from datetime import datetime

# ===================
# ExtractRegex Helper
# ===================
def identificar_tipo(texto: str) -> str:
    if "data consulta" in texto or "consulta" in texto:
        return "consulta"
    elif "data exame" in texto or "exame" in texto:
        return "exame"
    return "desconhecido"


# ================
# SaveStep Helper
# ================
def save_to_file(data, prefix="stage", folder="debug"):
    os.makedirs(folder, exist_ok=True)

    if isinstance(data, dict) or (isinstance(data, list) and all(isinstance(x, dict) for x in data)):
        ext = ".json"
        content = json.dumps(data, ensure_ascii=False, indent=2)
    else:
        ext = ".txt"
        content = "\n\n".join(data)

    out_path = os.path.join(folder, f"{prefix}{ext}")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"[DEBUG] Dump salvo em {out_path}")
    return out_path


# ================
# MergeDateTime Helper
# ================
def merge_date_and_time(data_iso: str, hora_str: str) -> str | None:
    """
    Junta data ISO ('2025-10-27T00:00:00Z') e hora ('10:25')
    em um único timestamp UTC ISO.
    """
    try:
        dt_data = datetime.fromisoformat(data_iso.replace("Z", ""))
        dt_hora = datetime.strptime(hora_str, "%H:%M").time()
        dt_final = datetime.combine(dt_data.date(), dt_hora)
        return dt_final.strftime("%Y-%m-%dT%H:%M:%SZ")
    except Exception:
        return None



def coletar_resultados(BASE_DIR):
    """
    Vasculha todas as subpastas e junta os resultados.json.
    Retorna lista única com todos os registros.
    """
    todos = []
    for root, dirs, files in os.walk(BASE_DIR):
        if "resultados.json" in files:
            caminho = os.path.join(root, "resultados.json")
            with open(caminho, "r", encoding="utf-8") as f:
                dados = json.load(f)
                todos.extend(dados)
    return todos

def separar_por_tipo(registros):
    """
    Divide registros em dois grupos: consultas e exames.
    Retorna dicionário {"consulta": [...], "exame": [...]}
    """
    separados = {"consulta": [], "exame": []}
    for r in registros:
        tipo = r.get("tipo")
        if tipo == "consulta":
            separados["consulta"].append(r)
        elif tipo == "exame":
            separados["exame"].append(r)
    return separados

def salvar_unificado(separados, BASE_DIR):
    """
    Salva arquivos unificados na raiz: consultas.json e exames.json
    """
    for tipo, lista in separados.items():
        out_path = os.path.join(BASE_DIR, f"{tipo}s.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(lista, f, ensure_ascii=False, indent=2)
        print(f"[OK] {len(lista)} registros salvos em {out_path}")

def consolidar_resultados(BASE_DIR):
    """
    Pipeline de consolidação:
      1. Coleta todos resultados.json
      2. Separa por tipo
      3. Salva na raiz
    """
    registros = coletar_resultados(BASE_DIR)
    separados = separar_por_tipo(registros)
    salvar_unificado(separados, BASE_DIR)



# ----------------------------------------------------------------------------------------------------------



def carregar_json(path):
    """Carrega lista de registros de um arquivo JSON."""
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def parse_time(r):
    """Converte timestamp em datetime; se inválido retorna datetime.min"""
    try:
        return datetime.fromisoformat(r.get("arquivo_created_utc", "").replace("Z", "+00:00"))
    except Exception:
        return datetime.min

def deduplicar(registros, tipo="consulta"):
    chaves = {}
    campo_ref = "especialidade" if tipo == "consulta" else "exame"

    for r in registros:
        codigo = r.get("codigo") or ""
        nome = r.get("nome") or ""
        campo = r.get(campo_ref) or ""
        ts = r.get("arquivo_created_utc", "")

        keys = [
            f"{codigo}|{campo}" if codigo else None,
            f"{nome}|{campo}" if nome else None
        ]

        for k in keys:
            if not k:
                continue
            atual = chaves.get(k)
            if not atual or ts > atual.get("arquivo_created_utc", ""):  # comparação direta
                chaves[k] = r

    return list({id(v): v for v in chaves.values()}.values())


def salvar_json(lista, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(lista, f, ensure_ascii=False, indent=2)
    print(f"[OK] {len(lista)} registros salvos em {path}")


def consolidar_firestore(BASE_DIR):
    """
    Pipeline:
      1. Carrega consultas.json e exames.json
      2. Deduplica cada um
      3. Junta tudo em data_firestore.json
    """
    consultas = carregar_json(os.path.join(BASE_DIR, "consultas.json"))
    exames = carregar_json(os.path.join(BASE_DIR, "exames.json"))

    consultas_dedup = deduplicar(consultas, "consulta")
    exames_dedup = deduplicar(exames, "exame")

    todos = consultas_dedup + exames_dedup
    salvar_json(todos, os.path.join(BASE_DIR, "data_firestore.json"))

