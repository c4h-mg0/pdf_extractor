# src/parsers/normalizers.py
from src.interfaces import BaseNormalizer
import re


class CodigoNormalizer(BaseNormalizer):
    campo = "codigo"

    def normalizar(self, valor: str) -> str:
        # ponto-chave: pega só os dígitos
        return re.sub(r"\D", "", valor)  


class NomeNormalizer(BaseNormalizer):
    campo = "nome"

    def normalizar(self, valor: str) -> str:
        if not valor:
            return None

        # 1. Substitui "!" por "i"
        valor = valor.replace("!", "i")

        # 2. Mantém apenas permitido: letras, ç, espaço, apóstrofo, hífen, símbolos
        permitido = r"[^a-zA-ZçÇ' \-€£¥₩₽]"
        valor = re.sub(permitido, "", valor)

        # 3. Remove letras soltas
        valor = re.sub(r"^[A-Za-zçÇ] ", "", valor)       # letra no início
        valor = re.sub(r" [A-Za-zçÇ]$", "", valor)       # letra no fim
        valor = re.sub(r" [A-Za-zçÇ] ", " ", valor)      # letra no meio

        # 4. Normaliza espaços
        valor = re.sub(r"\s+", " ", valor).strip()

        return valor if valor else None


class DataNascimentoNormalizer(BaseNormalizer):
    campo = "data_nascimento"

    def normalizar(self, valor: str) -> str:
        if not valor:
            return None

        # 1. Extrai apenas os números
        numeros = re.sub(r"\D", "", valor)

        # 2. Só aceita se tiver exatamente 8
        return numeros if len(numeros) == 8 else None


class CnsNormalizer(BaseNormalizer):
    campo = "cns"

    def normalizar(self, valor: str) -> str:
        if not valor:
            return None

        # 1. Extrai apenas os números
        numeros = re.sub(r"\D", "", valor)

        # 2. Só aceita se tiver exatamente 8
        return numeros if len(numeros) >= 15 else None


class DataConsultaNormalizer(BaseNormalizer):
    campo = "data_consulta"
    tipos = ["consulta"]

    def normalizar(self, valor: str) -> str:
        if not valor:
            return None

        # 1. Extrai apenas os números
        numeros = re.sub(r"\D", "", valor)

        # 2. Só aceita se tiver exatamente 8
        return numeros if len(numeros) == 8 else None


class DataExameNormalizer(BaseNormalizer):
    campo = "data_exame"
    tipos = ["exame"]

    def normalizar(self, valor: str) -> str:
        if not valor:
            return None

        # 1. Extrai apenas os números
        numeros = re.sub(r"\D", "", valor)

        # 2. Só aceita se tiver exatamente 8
        return numeros if len(numeros) == 8 else None


class HorarioNormalizer(BaseNormalizer):
    campo = "horario"

    def normalizar(self, valor: str) -> str:
        if not valor:
            return None

        # 1. Extrai apenas os números
        numeros = re.sub(r"\D", "", valor)

        # 2. Só aceita se tiver exatamente 8
        return numeros if len(numeros) == 4 else None


class ChegarAsNormalizer(BaseNormalizer):
    campo = "chegar_as"

    def normalizar(self, valor: str) -> str:
        if not valor:
            return None

        # 1. Extrai apenas os números
        numeros = re.sub(r"\D", "", valor)

        # 2. Só aceita se tiver exatamente 8
        return numeros if len(numeros) == 4 else None


class ProfissionalNormalizer(BaseNormalizer):
    campo = "profissional"
    tipos = ["consulta"]

    def normalizar(self, valor: str) -> str:
        if not valor:
            return None

        # 1. Substitui "!" por "i"
        valor = valor.replace("!", "i")

        # 2. Mantém apenas permitido: letras, ç, espaço, apóstrofo, hífen, símbolos
        permitido = r"[^a-zA-ZçÇ' \-€£¥₩₽]"
        valor = re.sub(permitido, "", valor)

        # 3. Remove letras soltas
        valor = re.sub(r"^[A-Za-zçÇ] ", "", valor)       # letra no início
        valor = re.sub(r" [A-Za-zçÇ]$", "", valor)       # letra no fim
        valor = re.sub(r" [A-Za-zçÇ] ", " ", valor)      # letra no meio

        # 4. Normaliza espaços
        valor = re.sub(r"\s+", " ", valor).strip()

        return valor if valor else None

class EspecialidadeNormalizer(BaseNormalizer):
    campo = "especialidade"
    tipos = ["consulta"]

    def normalizar(self, valor: str) -> str:
        if not valor:
            return None

        # 1. Substitui "!" por "i"
        valor = valor.replace("!", "i")

        # 2. Mantém apenas permitido: letras, ç, espaço, apóstrofo, hífen, símbolos
        permitido = r"[^a-zA-ZçÇ' \-€£¥₩₽]"
        valor = re.sub(permitido, "", valor)

        # 3. Remove letras soltas
        valor = re.sub(r"^[A-Za-zçÇ] ", "", valor)       # letra no início
        valor = re.sub(r" [A-Za-zçÇ]$", "", valor)       # letra no fim
        valor = re.sub(r" [A-Za-zçÇ] ", " ", valor)      # letra no meio

        # 4. Normaliza espaços
        valor = re.sub(r"\s+", " ", valor).strip()

        return valor if valor else None


class ExameNormalizer(BaseNormalizer):
    campo = "exame"
    tipos = ["exame"]

    def normalizar(self, valor: str) -> str:
        if not valor:
            return None

        # 1. Substitui "!" por "i"
        valor = valor.replace("!", "i")

        # 2. Mantém apenas permitido: letras, ç, espaço, apóstrofo, hífen, símbolos
        permitido = r"[^a-zA-ZçÇ' \-€£¥₩₽]"
        valor = re.sub(permitido, "", valor)

        # 3. Remove letras soltas
        valor = re.sub(r"^[A-Za-zçÇ] ", "", valor)       # letra no início
        valor = re.sub(r" [A-Za-zçÇ]$", "", valor)       # letra no fim
        valor = re.sub(r" [A-Za-zçÇ] ", " ", valor)      # letra no meio

        # 4. Normaliza espaços
        valor = re.sub(r"\s+", " ", valor).strip()

        return valor if valor else None


class LocalNormalizer(BaseNormalizer):
    campo = "local"

    def normalizar(self, valor: str) -> str:
        if not valor:
            return None

        # 1. Substitui "!" por "i"
        valor = valor.replace("!", "i")

        # 2. Mantém apenas permitido: letras, ç, espaço, apóstrofo, hífen, símbolos
        permitido = r"[^a-zA-ZçÇ' \-€£¥₩₽]"
        valor = re.sub(permitido, "", valor)

        # 3. Remove letras soltas
        valor = re.sub(r"^[A-Za-zçÇ] ", "", valor)       # letra no início
        valor = re.sub(r" [A-Za-zçÇ]$", "", valor)       # letra no fim
        valor = re.sub(r" [A-Za-zçÇ] ", " ", valor)      # letra no meio

        # 4. Normaliza espaços
        valor = re.sub(r"\s+", " ", valor).strip()

        return valor if valor else None


