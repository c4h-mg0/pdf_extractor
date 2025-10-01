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
