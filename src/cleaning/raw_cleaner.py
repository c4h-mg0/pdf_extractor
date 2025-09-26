import re
import unicodedata

from typing import Callable, List


# -----------------------------
# 🔹 Global
# -----------------------------
def remove_invisibles(text: str) -> str:
    """Remove caracteres de controle invisíveis."""
    return "".join(c for c in text if c.isprintable())
    
def remove_lixo(text: str) -> str:
    """Remove caracteres absurdos. Ex: !@#$%^&* etc."""
    # Mantém letras, números, espaços, pontuação básica
    return re.sub(r"[^A-Za-z0-9\s!'()=?:;.,/\-]", "", text)

def remove_accents(text: str) -> str:
    """Remove acentos mantendo letras."""
    nfkd = unicodedata.normalize("NFKD", text)
    return "".join([c for c in nfkd if not unicodedata.combining(c)])

def normalize_separators(text: str) -> str:
    """Troca separadores estranhos por ':' apenas em chave:valor."""
    return re.sub(r"\s*[;=]\s*", ": ", text)

def fix_spaces(text: str) -> str:
    """Remove espaços repetidos e antes/depois de pontuação."""
    text = re.sub(r"\s+", " ", text)       # espaços múltiplos → 1
    text = re.sub(r"\s+([:/\-])", r"\1", text)  # tira espaço antes de / ou -
    return text.strip()


# -----------------------------
# 🔹 Função Principal
# -----------------------------
def clean_raw(text: str) -> str:
    """Aplica todas as limpezas na ordem certa."""
    text = remove_invisibles(text)
    text = remove_accents(text)
    text = normalize_separators(text)
    text = fix_spaces(text)
    text = remove_lixo(text)   

    return text
