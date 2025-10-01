# src/parsers/normalizers.py
from src.parsers.base_normalizers import DigitsNormalizer, TextoNormalizer


# ---- Campos numéricos ----
class CodigoNormalizer(DigitsNormalizer):
    campo = "codigo"


class DataNascimentoNormalizer(DigitsNormalizer):
    campo = "data_nascimento"
    tamanho=8


class CnsNormalizer(DigitsNormalizer):
    campo = "cns"
    minimo = {15, 30, 45, 60, 75}

class DataConsultaNormalizer(DigitsNormalizer):
    campo = "data_consulta"
    tamanho=8
    tipos = ["consulta"]


class DataExameNormalizer(DigitsNormalizer):
    campo = "data_exame"
    tamanho=8
    tipos = ["exame"]


class HorarioNormalizer(DigitsNormalizer):
    campo = "horario"
    tamanho=4


class ChegarAsNormalizer(DigitsNormalizer):
    campo = "chegar_as"
    tamanho=4


# ---- Campos de texto ----
class NomeNormalizer(TextoNormalizer):
    campo = "nome"


class ProfissionalNormalizer(TextoNormalizer):
    campo = "profissional"
    tipos = ["consulta"]


class EspecialidadeNormalizer(TextoNormalizer):
    campo = "especialidade"
    tipos = ["consulta"]


class ExameNormalizer(TextoNormalizer):
    campo = "exame"
    tipos = ["exame"]


class LocalNormalizer(TextoNormalizer):
    campo = "local"

