# src/parsers/extractors.py
import re
from src.interfaces import BaseExtractor


class CodigoExtractor(BaseExtractor):
    campo = "codigo"

    def extrair(self, texto: str):
        regex = r"c[o0]digo\s*[:;.,-]?\s*([\d\s.,]{3,12})"
        match = re.search(regex, texto)
        return match.group(1).splitlines()[0].strip() if match else None


class NomeExtractor(BaseExtractor):
    campo = "nome"

    def extrair(self, texto: str):
        match = re.search(r"(?:nome|neme)\s*[:;.,]?\s*([a-z '!\-]+)", texto)
        return match.group(1).strip().split("\n")[0] if match else None


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




# class TipoExtractor(BaseExtractor):
#     def extrair(self, texto: str):
#         # captura "especialidade" ou "exame"
#         match = re.search(
#             r"(especialidade|exame)\s*[:;.,-]?\s*([a-z0-9\s\-\(\)]+)",
#             texto,
#             re.IGNORECASE
#         )
#         if match:
#             tipo = match.group(1).lower()  # "especialidade" ou "exame"
#             valor = match.group(2).strip().split("\n")[0]
#             return {tipo: valor}
#         return None

# class DataExtractor(BaseExtractor):
#     def extrair(self, texto: str):
#         # tenta capturar "data consulta" ou "data exame"
#         match = re.search(
#             r"(data\s*(consulta|exame))\s*[:;.,-]?\s*([\d\s\-]+)",
#             texto,
#             re.IGNORECASE
#         )
#         if match:
#             tipo = match.group(2).lower()   # "consulta" ou "exame"
#             valor = match.group(3).strip().split("\n")[0]
#             valor = self.normalizar_data(valor)
#             return {f"data_{tipo}": valor}
#         return None

#     def normalizar_data(self, valor: str) -> str:
#         # remove espaços extras
#         valor = valor.replace(" ", "")
#         # se já estiver DD-MM-YYYY, retorna padronizado
#         if re.match(r"^\d{2}-\d{2}-\d{4}$", valor):
#             return valor
#         return valor  # fallback cru
