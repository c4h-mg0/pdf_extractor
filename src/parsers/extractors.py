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


