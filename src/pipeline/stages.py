# src/parse_steps/pipeline_parser.py
from src.ocr.pdf_ocr import PdfOCR
from src.interfaces import Step, BaseExtractor
from src.parsers.cleaners import *
import os
import json


class RunOcr(Step):
    def __init__(self, dpi=400, lang="por"):

        self.dpi = dpi
        self.lang = lang
    
    def processar(self, pdf_path: str) -> list[str]:
        ocr_engine = PdfOCR(dpi=self.dpi, lang=self.lang)
        paginas = ocr_engine.extract(pdf_path)
        return paginas


class Cleaner(Step):     
    def processar(self, paginas: list[str]) -> list[str]:
        paginas_limpas = []
        for texto in paginas:
            texto = remover_invisiveis(texto)
            texto = remover_acentos(texto)
            texto = texto_lower(texto)
            texto = ajustar_espacos(texto)
            paginas_limpas.append(texto)
        return paginas_limpas

 
class ExtractRegex:
    def processar(self, blocos: list[str]) -> list[dict]:
        resultado_total = []
        for bloco in blocos:
            tipo = identificar_tipo(bloco)
            dados = {"tipo": tipo}

            # roda os extractors relevantes
            for extractor in BaseExtractor.registry:
                if tipo in extractor.tipos:
                    dados[extractor.campo] = extractor.extrair(bloco)

            # garante que todos os campos daquele tipo apareçam, mesmo se None
            obrigatorios = [
                e.campo for e in BaseExtractor.registry if tipo in e.tipos
            ]
            for campo in obrigatorios:
                if campo not in dados:
                    dados[campo] = None

            resultado_total.append(dados)
        return resultado_total


def identificar_tipo(texto: str) -> str:
    if "data consulta" in texto or "consulta" in texto:
        return "consulta"
    elif "data exame" in texto or "exame" in texto:
        return "exame"
    return "desconhecido"




class SaveStep(Step):
    def __init__(self, step_name, prefix="stage", base_folder="debug", final=False):
        """
        step_name -> nome da etapa (ex.: OCRStep, Cleaner)
        prefix    -> prefixo do arquivo (ex.: 01_OCRStep)
        base_folder -> pasta raiz de debug
        final     -> se True, trata como resultado final consolidado
        """
        self.prefix = prefix
        self.folder = os.path.join(base_folder, step_name)
        self.final = final
        os.makedirs(self.folder, exist_ok=True)

    def _next_index(self, ext):
        files = os.listdir(self.folder)
        count = sum(1 for f in files if f.startswith(self.prefix) and f.lower().endswith(ext.lower()))
        return count + 1

    def processar(self, data):
        # se for a etapa final -> sempre salva JSON bonitinho
        if self.final:
            ext = ".json"
            content = json.dumps(data, ensure_ascii=False, indent=2)

        # fluxo normal
        elif isinstance(data, list) and all(isinstance(x, str) for x in data):
            ext = ".txt"
            blocks = []
            for i, page in enumerate(data, start=1):
                blocks.append(f"\n----- PÁGINA {i:03d} -----\n{page.strip()}")
            content = "\n".join(blocks)

        elif isinstance(data, list) and all(isinstance(x, dict) for x in data):
            ext = ".json"
            content = json.dumps(data, ensure_ascii=False, indent=2)

        elif isinstance(data, dict):
            ext = ".json"
            content = json.dumps(data, ensure_ascii=False, indent=2)

        elif isinstance(data, str):
            ext = ".txt"
            content = data

        else:
            ext = ".json"
            content = json.dumps(data, ensure_ascii=False, indent=2)

        idx = self._next_index(ext)
        out_name = f"{self.prefix}_{idx:03d}{ext}"
        out_path = os.path.join(self.folder, out_name)

        with open(out_path, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"[DEBUG] Dump salvo em {out_path}")
        return data




def with_debug(steps, base_folder="debug"):
    debugged = []
    for i, step in enumerate(steps, start=1):
        step_name = step.__class__.__name__
        is_last = (i == len(steps))  # última etapa do pipeline
        debugged.append(step)
        debugged.append(
            SaveStep(
                step_name=step_name,
                prefix=f"{i:02d}_{step_name}",
                base_folder=base_folder,
                final=is_last
            )
        )
    return debugged

