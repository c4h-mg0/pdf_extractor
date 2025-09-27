# src/extractor/base_extractor.py
import re

# Registry global
EXTRACTORS = []

class BaseExtractor:
    campo = None   # nome do campo (ex: "codigo", "nome")

    def __init_subclass__(cls, **kwargs):
        """
        Toda subclasse registrada automaticamente no Registry.
        """
        super().__init_subclass__(**kwargs)
        if cls.campo:  
            EXTRACTORS.append(cls())

    def extrair(self, texto: str):
        raise NotImplementedError
