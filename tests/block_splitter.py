# src/parser_steps/data_blocks.py
from src.parse_steps.interface import Step


class BlockSplitter(Step):
    """
    Divide o texto em blocos por página.
    Cada página corresponde exatamente a um bloco de texto.
    """

    def processar(self, texto: str) -> list[str]:
        # Divide o texto em páginas (usando \f como separador)
        paginas = texto.split("\f")
        blocos = []

        for pagina in paginas:
            pagina = pagina.strip()
            if pagina:  # ignora páginas vazias
                blocos.append(pagina)

        return blocos



        # parser_steps/split_blocks.py
import re
from .step import Step

class SplitBlocks(Step):
    def processar(self, texto: str) -> list[dict]:
        """
        Divide o texto em blocos de pacientes/páginas.
        Ordem de fallback:
        1. codigo:
        2. local:
        3. quebra dupla de linha
        Retorna: [{"texto": str, "split_por": str}, ...]
        """
        blocos = []
        metodo = None

        # 1. Tenta com "codigo:"
        partes = re.split(r"(?=codigo:)", texto)
        partes = [p.strip() for p in partes if p.strip()]
        if len(partes) > 1:
            metodo = "codigo"
            blocos = partes

        # 2. Fallback: usa "local:"
        if not blocos:
            partes = re.split(r"(?=local:)", texto)
            partes = [p.strip() for p in partes if p.strip()]
            if len(partes) > 1:
                metodo = "local"
                blocos = partes

        # 3. Fallback final: divide por linha em branco
        if not blocos:
            partes = re.split(r"\n\s*\n", texto)
            partes = [p.strip() for p in partes if p.strip()]
            if len(partes) > 1:
                metodo = "paragrafo"
                blocos = partes

        # Se nada dividiu, retorna tudo como 1 bloco
        if not blocos:
            metodo = "unico"
            blocos = [texto.strip()] if texto.strip() else []

        # monta saída
        return [{"texto": b, "split_por": metodo} for b in blocos]



# parser_steps/extract_regex.py
from .step import Step
from .extractors import EXTRACTORS

class ExtractRegex(Step):
    def processar(self, blocos: list[dict]) -> list[dict]:
        """
        Recebe blocos já separados e aplica regex para extrair campos.
        Cada resultado inclui qual método de split foi usado.
        """
        resultado_total = []
        for bloco in blocos:
            dados = {"split_por": bloco["split_por"]}
            for extractor in EXTRACTORS:
                dados[extractor.campo] = extractor.extrair(bloco["texto"])
            resultado_total.append(dados)
        return resultado_total



# parser_steps/split_blocks.py
import re
from src.interfaces import Step

class SplitBlocks(Step):
    def processar(self, texto: str) -> list[dict]:
        """
        Divide o texto em blocos de pacientes/páginas.
        Ordem de fallback:
        1. codigo:
        2. local:
        3. quebra dupla de linha
        Retorna: [{"texto": str, "split_por": str}, ...]
        """
        blocos, metodo = [], None

        # 1. codigo:
        partes = re.split(r"(?=codigo:)", texto)
        partes = [p.strip() for p in partes if p.strip()]
        if len(partes) > 1:
            metodo, blocos = "codigo", partes

        # 2. local:
        if not blocos:
            partes = re.split(r"(?=local:)", texto)
            partes = [p.strip() for p in partes if p.strip()]
            if len(partes) > 1:
                metodo, blocos = "local", partes

        # 3. parágrafo
        if not blocos:
            partes = re.split(r"\n\s*\n", texto)
            partes = [p.strip() for p in partes if p.strip()]
            if len(partes) > 1:
                metodo, blocos = "paragrafo", partes

        # 4. único bloco
        if not blocos:
            metodo = "unico"
            blocos = [texto.strip()] if texto.strip() else []

        return [{"texto": b, "split_por": metodo} for b in blocos]




def process_pdf(pdf_path, debug=False):
    steps = [
        OCRStep(dpi=400, lang="por"),
        Cleaner(),
        ExtractRegex(),
    ]

    if debug:
        steps = [
            OCRStep(dpi=400, lang="por"),
            SaveStep(prefix="01_ocr"),
            Cleaner(),
            SaveStep(prefix="02_clean"),
            ExtractRegex(),
            SaveStep(prefix="03_final"),
        ]

    pipeline = ParsePipeline(steps)
    return pipeline.run(pdf_path)


class Cleaner(Step):
    def __init__(self, debug_prefix=None):
        self.debug_prefix = debug_prefix

    def processar(self, texto: str) -> str:
        texto = texto.strip()
        # salva dump se debug estiver ativado
        if self.debug_prefix:
            SaveStep(prefix=self.debug_prefix).processar(texto)
        return texto


steps = [
    OCRStep(dpi=400, lang="por", debug_prefix="01_ocr"),
    Cleaner(debug_prefix="02_clean"),
    ExtractRegex(debug_prefix="03_final"),
]


def with_debug(steps, folder="debug"):
    debugged = []
    for i, step in enumerate(steps, start=1):
        debugged.append(step)
        debugged.append(SaveStep(prefix=f"{i:02d}_{step.__class__.__name__}", folder=folder))
    return debugged


steps = [
    OCRStep(),
    Cleaner(),
    ExtractRegex(),
]

pipeline = ParsePipeline(with_debug(steps))
pipeline.run(pdf_path)


# src/steps/save_step.py (pode ficar junto do SaveStep)

def with_debug(steps, folder="debug"):
    """
    Insere SaveSteps entre cada etapa do pipeline.
    Exemplo:
      [OCRStep(), Cleaner()] ->
      [OCRStep(), SaveStep("01_OCRStep"), Cleaner(), SaveStep("02_Cleaner")]
    """
    debugged = []
    for i, step in enumerate(steps, start=1):
        debugged.append(step)
        debugged.append(SaveStep(prefix=f"{i:02d}_{step.__class__.__name__}", folder=folder))
    return debugged


# src/pipeline/processor_pipeline.py
from src.pipeline.pipeline import ParsePipeline
from src.steps.ocr_step import OCRStep
from src.steps.cleaner import Cleaner
from src.steps.extract_regex import ExtractRegex
from src.steps.save_step import with_debug


def process_pdf(pdf_path, debug=False):
    """
    Executa o pipeline completo em um PDF.
    Se debug=True, injeta SaveSteps após cada etapa.
    """
    steps = [
        OCRStep(dpi=400, lang="por"),
        Cleaner(),
        ExtractRegex(),
    ]

    if debug:
        steps = with_debug(steps, folder="debug")

    pipeline = ParsePipeline(steps)
    return pipeline.run(pdf_path)



class CodigoExtractor(BaseTextExtractor):
    campo = "codigo"

    def extrair(self, texto: str):
        match = re.search(r"(?:codigo|corigo)\s*[:;.,]?\s*([\d\s.,-]{3,})", texto, re.IGNORECASE)
        if match:
            valor = self.normalizar_codigo(match.group(1))
            return {self.campo: valor}
        return None



from abc import ABC, abstractmethod

class BaseTextExtractor(ABC):
    """
    Extrator base: todo extractor retorna sempre um dict.
    """

    campo = None  # usado nos casos simples (ex.: "codigo")

    @abstractmethod
    def extrair(self, texto: str) -> dict:
        """
        Retorna sempre um dict. Ex:
        - {"codigo": "12345"}
        - {"data_consulta": "12-10-2025"}
        - {}
        """
        pass

    def pos_processar(self, valor: str) -> str:
        """Hook para normalizações simples (override se precisar)."""
        return valor.strip() if valor else valor



class CodigoExtractor(BaseTextExtractor):
    campo = "codigo"

    def extrair(self, texto: str):
        import re
        match = re.search(r"(?:codigo|corigo)\s*[:;.,]?\s*([\d\s.,-]{3,12})", texto, re.IGNORECASE)
        if match:
            valor = self.pos_processar(match.group(1))
            return {self.campo: valor}
        return {}


class DataExtractor(BaseTextExtractor):
    def extrair(self, texto: str):
        import re
        match = re.search(r"(data\s*(consulta|exame))\s*[:;.,-]?\s*([\d\s\-]+)", texto, re.IGNORECASE)
        if match:
            tipo = match.group(2).lower()       # consulta ou exame
            valor = self.pos_processar(match.group(3))
            return {f"data_{tipo}": valor}
        return {}


dados = {}
for extractor in EXTRACTORS:
    dados.update(extractor.extrair(bloco))  # junta todos os dicts
