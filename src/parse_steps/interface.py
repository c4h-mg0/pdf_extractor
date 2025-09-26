# etapas/base.py
class Step:
    def processar(self, entrada):
        """Toda etapa deve implementar esse método"""
        raise NotImplementedError("Subclasses devem implementar processar()")



