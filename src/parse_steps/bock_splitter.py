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
