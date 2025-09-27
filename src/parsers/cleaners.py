# src/parsers/cleaners.py
import re
import unicodedata


def remover_invisiveis(texto: str) -> str:
    """Remove caracteres de controle não imprimíveis, preservando \n"""
    return "".join(ch for ch in texto if ch.isprintable() or ch == "\n")

def remover_acentos(texto: str) -> str:
    """Remove acentos mantendo apenas letras ASCII"""
    nfkd = unicodedata.normalize("NFKD", texto)
    return "".join(c for c in nfkd if not unicodedata.combining(c))

def ajustar_espacos(texto: str) -> str:
    """Remove espaços repetidos e antes/depois de pontuação sem matar \n"""
    texto = re.sub(r"[ \t]+([:/\-])", r"\1", texto)   # espaço antes de : / -
    texto = re.sub(r"[ \t]{2,}", " ", texto)          # múltiplos espaços -> um
    return "\n".join(line.strip() for line in texto.splitlines())

def texto_lower(texto: str) -> str:
    return texto.lower()
