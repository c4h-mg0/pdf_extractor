# src/parsers/extractors.py
import re
from src.interfaces import BaseExtractor



# -------------------
# Extractors comuns
# -------------------
class CodigoExtractor(BaseExtractor):
    campo = "codigo"

    def extrair(self, texto: str):
        match = re.search(r"c[o0]digo\s*[:;.,-]?\s*([\d\s]{3,12})", texto)
        return match.group(1).strip() if match else None


class NomeExtractor(BaseExtractor):
    campo = "nome"

    def extrair(self, texto: str):
        match = re.search(r"nome\s*[:;.,]?\s*([a-z '!\-]+)", texto)
        return match.group(1).split("\n")[0].strip() if match else None


class LocalExtractor(BaseExtractor):
    campo = "local"

    def extrair(self, texto: str):
        match = re.search(r"local[:\s]*(.+)", texto)
        return match.group(1).split("\n")[0].strip() if match else None

class ProfissionalExtractor(BaseExtractor):
    campo = "profissional"

    def extrair(self, texto: str):
        match = re.search(r"profissional[:\s]*([^\n\r]+)", texto)
        return match.group(1).split("\n")[0].strip() if match else None

class HorarioExtractor(BaseExtractor):
    campo = "horario"

    def extrair(self, texto: str):
        match = re.search(r"horario[:\s]*([0-2]?\d:[0-5]\d)", texto)
        return match.group(1).split("\n")[0].strip() if match else None

class ChegarAsExtractor(BaseExtractor):
    campo = "chegar_as"

    def extrair(self, texto: str):
        match = re.search(r"chegar[^\d]*?([0-2]?\d:[0-5]\d)", texto)
        return match.group(1).split("\n")[0].strip() if match else None

class CnsExtractor(BaseExtractor):
    campo = "cns"

    def extrair(self, texto: str):
        match = re.search(r"cns[:\s]*([\d,\s]+)", texto)
        return match.group(1).split("\n")[0].strip() if match else None

class DataNascimentoExtractor(BaseExtractor):
    campo = "data_nascimento"

    def extrair(self, texto: str):
        # procura "data de nascimento" ou apenas "nascimento"
        match = re.search(r"(?:data\s*de\s*)?nascimento\s*[:;.,]?\s*([0-9\s/]+)", texto)
        if match:
            valor = match.group(1)
            # remove espaços extras e símbolos estranhos
            valor = re.sub(r"\s+", "", valor)
            return valor  # exemplo: "13081984"
        return None

# -------------------
# Extractor tipo: Consulta
# -------------------
class EspecialidadeExtractor(BaseExtractor):
    campo = "especialidade"
    tipos = ["consulta"]

    def extrair(self, texto: str):
        match = re.search(r"especialidade\s*[:;.,-]?\s*([a-z ]+)", texto)
        return match.group(1).strip() if match else None


class DataConsultaExtractor(BaseExtractor):
    campo = "data_consulta"
    tipos = ["consulta"]

    def extrair(self, texto: str):
        regex = r"(?:data\s*)?consulta\s*[:;.,-]?\s*([\d/-]{8,10})"
        match = re.search(regex, texto)
        return match.group(1).strip() if match else None


# -------------------
#  Extractor tipo: Exame
# -------------------
class ExameExtractor(BaseExtractor):
    campo = "exame"
    tipos = ["exame"]

    def extrair(self, texto: str):
        # procura "data exame" para começar do ponto correto
        pos_data = texto.find("data exame")
        if pos_data == -1:
            return None

        fragmento = texto[pos_data:].splitlines()

        for linha in fragmento:
            # ignora linhas que não contenham "exame" seguido de valor
            match = re.match(r"exame\s*[:;,.\-\s]?\s*(.+)", linha, re.IGNORECASE)
            if match:
                # captura apenas o valor depois de "exame"
                return match.group(1).strip()

        return None


class DataExameExtractor(BaseExtractor):
    campo = "data_exame"
    tipos = ["exame"]

    def extrair(self, texto: str):
        regex = r"(?:data\s*)?exame\s*[:;.,-]?\s*([\d/-]{8,10})"
        match = re.search(regex, texto)
        return match.group(1).strip() if match else None


