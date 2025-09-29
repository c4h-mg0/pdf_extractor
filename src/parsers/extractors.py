# src/parsers/extractors.py
import re
from src.interfaces import BaseExtractor



class CodigoExtractor(BaseExtractor):
    campo = "codigo"

    def extrair(self, texto: str):
        regex = r"(?:c[o0]digo|c[o0]di|[o0]dig)[:\s]*(?:([^\n\r]+)|([^\n\r]+?)(?=\s*(?:nome|neme|$)))"
        match = re.search(regex, texto, re.I)
        return (match.group(1) or match.group(2)).strip() if match else None


class NomeExtractor(BaseExtractor):
    campo = "nome"

    def extrair(self, texto: str):
        regex = r"(?:nome|neme|ome)[:\s]*(?:([^\n\r]+)|([^\n\r]+?)(?=\s*(?:data\s*de\s*nascimento|nascimento|data|$)))"
        match = re.search(regex, texto, re.I)
        return (match.group(1) or match.group(2)).strip() if match else None


class DataNascimentoExtractor(BaseExtractor):
    campo = "data_nascimento"

    def extrair(self, texto: str):
        regex = r"(?:data\s*de\s*)?nascimento[:\s]*(?:([^\n\r]+)|([^\n\r]+?)(?=\s*(?:cns|ens|$)))"
        match = re.search(regex, texto, re.I)
        return (match.group(1) or match.group(2)).strip() if match else None


class CnsExtractor(BaseExtractor):
    campo = "cns"

    def extrair(self, texto: str):
        regex = r"(?:cns|ens)[:\s]*(?:([^\n\r]+)|([^\n\r]+?)(?=\s*(?:telefone|comercial|$)))"
        match = re.search(regex, texto, re.I)
        return (match.group(1) or match.group(2)).strip() if match else None


class DataConsultaExtractor(BaseExtractor):
    campo = "data_consulta"
    tipos = ["consulta"]

    def extrair(self, texto: str):
        regex = r"data\s*(?:consulta|con)[:\s]*(?:([^\n\r]+)|([^\n\r]+?)(?=\s*(?:horario|$)))"
        match = re.search(regex, texto, re.I)
        return (match.group(1) or match.group(2)).strip() if match else None


class DataExameExtractor(BaseExtractor):
    campo = "data_exame"
    tipos = ["exame"]

    def extrair(self, texto: str):
        regex = r"data\s*(?:exame|ex)[:\s]*(?:([^\n\r]+)|([^\n\r]+?)(?=\s*(?:horario|$)))"
        match = re.search(regex, texto, re.I)
        return (match.group(1) or match.group(2)).strip() if match else None


class HorarioExtractor(BaseExtractor):
    campo = "horario"

    def extrair(self, texto: str):
        regex = r"(?:h?orario)[:\s]*(?:([^\n\r]+)|([^\n\r]+?)(?=\s*(?:chegar|$)))"
        match = re.search(regex, texto, re.I)
        return (match.group(1) or match.group(2)).strip() if match else None


class ChegarAsExtractor(BaseExtractor):
    campo = "chegar_as"

    def extrair(self, texto: str):
        regex = r"chegar[^\d\n\r]*(?:([^\n\r]+)|([^\n\r]+?)(?=\s*(?:ssonal|prof|exame|local|$)))"
        match = re.search(regex, texto, re.I)
        return (match.group(1) or match.group(2)).strip() if match else None


class ProfissionalExtractor(BaseExtractor):
    campo = "profissional"
    tipos = ["consulta"]

    def extrair(self, texto: str):
        regex = r"prof\w*\s*[:;,.\s]\s*([^\n\r]+?)(?=\s*(?:especialidade|specialidade|$))"
        match = re.search(regex, texto, re.I)
        return (match.group(1) or match.group(2)).strip() if match else None


class EspecialidadeExtractor(BaseExtractor):
    campo = "especialidade"
    tipos = ["consulta"]

    def extrair(self, texto: str):
        regex = r"(?:e?specialidad[ea])[:\s]*(?:([^\n\r]+)|([^\n\r]+?)(?=\s*(?:tipo|local|$)))"
        match = re.search(regex, texto, re.I)
        return (match.group(1) or match.group(2)).strip() if match else None


class ExameExtractor(BaseExtractor):
    campo = "exame"
    tipos = ["exame"]

    def extrair(self, texto: str):
        pos_data = texto.find("data exame")
        if pos_data == -1:
            return None

        fragmento = texto[pos_data:].splitlines()

        for linha in fragmento:
            if re.match(r"data\s*exame", linha, re.I):
                continue

            regex = r"^\s*exame[:\s]*(?:([^\n\r]+)|([^\n\r]+?)(?=\s*(?:local|endereco|$)))"
            match = re.search(regex, linha, re.I)
            if match:
                return (match.group(1) or match.group(2)).strip()

        return None


class LocalExtractor(BaseExtractor):
    campo = "local"

    def extrair(self, texto: str):
        regex = r"local[:\s]*(?:([^\n\r]+)|([^\n\r]+?)(?=\s*(?:endere|rua|$)))"
        match = re.search(regex, texto, re.I)
        return (match.group(1) or match.group(2)).strip() if match else None




