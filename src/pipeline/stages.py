# src/pipeline/stages.py
from src.ocr.pdf_ocr import PdfOCR
from src.interfaces import Step, BaseExtractor, BaseNormalizer, BaseTransformer
from src.parsers.cleaners import *
from src.pipeline.helpers import identificar_tipo, save_to_file, merge_date_and_time 


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


class ExtractRegex(Step):
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


class NormalizerRegex(Step):
    def processar(self, dados_lista: list[dict]) -> list[dict]:
        resultado_total = []

        for dados in dados_lista:
            # já existe, não precisa recriar
            tipo = dados["tipo"]

            # copia os dados originais
            normalizados = dict(dados)

            for normalizer in BaseNormalizer.registry:
                if tipo in normalizer.tipos:
                    valor = dados.get(normalizer.campo)
                    normalizados[normalizer.campo] = normalizer.normalizar(valor)

            # garante que todos os campos daquele tipo apareçam, mesmo se None
            obrigatorios = [
                e.campo for e in BaseNormalizer.registry if tipo in e.tipos
            ]
            for campo in obrigatorios:
                if campo not in normalizados:
                    normalizados[campo] = None

            resultado_total.append(normalizados)
        return resultado_total



class TransformStep(Step):
    """
    Step que aplica os transformers nos registros extraídos,
    respeitando o tipo do registro.
    """
    def processar(self, registros: list[dict]) -> list[dict]:
        for registro in registros:
            tipo = registro.get("tipo")
            for transformer in BaseTransformer.registry:
                # aplica só se o campo existe + tipo for compatível
                if (
                    tipo in transformer.tipos
                    and transformer.campo in registro
                    and registro[transformer.campo] is not None
                ):
                    registro[transformer.campo] = transformer.transformar(
                        registro[transformer.campo]
                    )
        return registros


class MergeDateTimeStep(Step):
    """
    Junta campos de data e horário em um timestamp UTC.
    Remove os campos originais depois de gerar o campo final.
    """
    def processar(self, registros: list[dict]) -> list[dict]:
        for registro in registros:
            tipo = registro.get("tipo")

            if tipo == "consulta":
                data = registro.pop("data_consulta", None)
                hora = registro.pop("horario", None)
                if data and hora:
                    registro["data_horario_consulta"] = merge_date_and_time(data, hora)

            elif tipo == "exame":
                data = registro.pop("data_exame", None)
                hora = registro.pop("horario", None)
                if data and hora:
                    registro["data_horario_exame"] = merge_date_and_time(data, hora)

        return registros


class SaveStep(Step):
    _counter = 0  # contador global para todos os SaveStep

    def __init__(self, prefix="stage", folder="debug"):
        self.prefix = prefix
        self.folder = folder

    def processar(self, data):
        SaveStep._counter += 1             # PONTO-CHAVE: incrementa a cada dump
        prefix = f"{self.prefix}_{SaveStep._counter:03d}"
        save_to_file(data, prefix=prefix, folder=self.folder)
        return data
