from src.interfaces import BaseTransformer
from datetime import datetime
import re

class DataNascimentoTransformer(BaseTransformer):
    campo = "data_nascimento"
    
    def transformar(self, valor: str) -> str:
        """
        Converte 'DDMMYYYY' em UTC timestamp (ISO 8601).
        Ex: '10052003' -> '2003-05-10T00:00:00Z'
        """
        try:
            dt = datetime.strptime(valor, "%d%m%Y")
            return dt.strftime("%Y-%m-%dT%H:%M:%SZ")
        except ValueError:
            return None  # falha -> deixa nulo


class DataConsulta(BaseTransformer):
    campo = "data_consulta"
    tipos = ["consulta"]
    
    def transformar(self, valor: str) -> str:
        """
        Converte 'DDMMYYYY' em UTC timestamp (ISO 8601).
        Ex: '10052003' -> '2003-05-10T00:00:00Z'
        """
        try:
            dt = datetime.strptime(valor, "%d%m%Y")
            return dt.strftime("%Y-%m-%dT%H:%M:%SZ")
        except ValueError:
            return None  # falha -> deixa nulo


class DataExame(BaseTransformer):
    campo = "data_exame"
    tipos = ["exame"]

    def transformar(self, valor: str) -> str:
        """
        Converte 'DDMMYYYY' em UTC timestamp (ISO 8601).
        Ex: '10052003' -> '2003-05-10T00:00:00Z'
        """
        try:
            dt = datetime.strptime(valor, "%d%m%Y")
            return dt.strftime("%Y-%m-%dT%H:%M:%SZ")
        except ValueError:
            return None  # falha -> deixa nulo


class HorarioTransformer(BaseTransformer):
    campo = "horario"

    def transformar(self, valor: str) -> str:
        """
        Converte 'HHMM' em 'HH:MM'.
        Ex: '1025' -> '10:25'
        """
        try:
            dt = datetime.strptime(valor, "%H%M")
            return dt.strftime("%H:%M")
        except ValueError:
            return None


class ChegarAsTransformer(BaseTransformer):
    campo = "chegar_as"

    def transformar(self, valor: str) -> str:
        """
        Converte 'HHMM' em 'HH:MM'.
        Ex: '1025' -> '10:25'
        """
        try:
            dt = datetime.strptime(valor, "%H%M")
            return dt.strftime("%H:%M")
        except ValueError:
            return None



class CnsTransformer(BaseTransformer):
    campo = "cns"

    def transformar(self, valor: str) -> str:
        """
        Insere espaço a cada 15 dígitos.
        Ex: '123456789012345123456789012345'
            -> '123456789012345 123456789012345'
        """
        if not valor:
            return None
        numeros = re.sub(r"\D", "", valor)  # garante só dígitos
        if not numeros:
            return None
        # ponto-chave: fatia de 15 em 15 e junta com espaço
        return " ".join(numeros[i:i+15] for i in range(0, len(numeros), 15))
