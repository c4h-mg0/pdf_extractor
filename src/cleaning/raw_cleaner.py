import re
import unicodedata

def remove_lixo(text: str) -> str:
    """Remove caracteres absurdos. Ex: !@#$%^&* etc."""
    # Mantém letras, números, espaços, pontuação básica
    return re.sub(r"[^A-Za-z0-9\s:;.,/\-]", "", text)

def normalize_separators(text: str) -> str:
    """
    Troca qualquer separador estranho (;, =, etc.) por :
    Mas só quando estiver no padrão chave:valor
    """
    # Troca ; ou = por :
    return re.sub(r"\s*[;=]\s*", ": ", text)

def fix_spaces(text: str) -> str:
    """Remove espaços repetidos e espaços antes/depois de pontuação."""
    text = re.sub(r"\s+", " ", text)  # espaços múltiplos → 1 espaço
    text = re.sub(r"\s+([:/\-])", r"\1", text)  # tira espaço antes de / ou -
    return text.strip()

def remove_accents(text: str) -> str:
    """Remove acentos mantendo as letras."""
    nfkd = unicodedata.normalize("NFKD", text)
    return "".join([c for c in nfkd if not unicodedata.combining(c)])

def fix_dates(text: str) -> str:
    """Padroniza datas: remove espaços errados e converte para dd/mm/yyyy. """
    # Remove espaços dentro de números: 3 0 → 30
    text = re.sub(r"(\d)\s+(\d)", r"\1\2", text)
    # Converte - para /
    text = re.sub(r"(\d)-(\d)", r"\1/\2", text)
    return text

def clean_raw(text: str) -> str:
    """Aplica todas as limpezas na ordem certa."""
    text = remove_accents(text)       # 1️⃣ tira só acentos
    text = remove_lixo(text)          # 2️⃣ remove símbolos absurdos
    text = normalize_separators(text)
    text = fix_spaces(text)
    text = fix_dates(text)
    return text
