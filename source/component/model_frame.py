"""
Componente de Frame já possuindo as seguintes customizações:
    -
"""

import ttkbootstrap as ttk

import source.styles as styles


class ModelFrame(ttk.Frame):

    parent = None # Janela pai.

    # Método construtor.
    # ├─ parent: janela pai.
    # └─ **kwargs: parâmetros extras.
    def __init__(self, parent, **kwargs)->None:

        self.parent = parent

        super().__init__(
            self.parent, # Janela pai.
            relief = kwargs.pop("relief", "solid"),
            padding = kwargs.pop("padding", (styles.PADDING_LARGE, styles.PADDING_MEDIUM)), # Espaçamento interno.
            takefocus = kwargs.pop("takefocus", False), # Desabilita a possibilidade deste widget receber foco.
            **kwargs # Parâmetros extras.
        )
        

    # Sobrescreve o método "pack()" da super classe.
    # └─ **kwargs: parâmetros extras.
    def pack(self, **kwargs)->None:
        super().pack(
            padx = kwargs.pop("padx", styles.PADDING_MEDIUM), # Espaçamento externo x.
            pady = kwargs.pop("pady", styles.PADDING_MEDIUM), # Espaçamento externo y.
            **kwargs
        )

    # Sobrescreve o método "grid()" da super classe.
    # ├─ row: número da linha.
    # ├─ column: número da coluna.
    # └─ **kwargs: parâmetros extras.
    def grid(self, row:int, column:int, **kwargs)->None:
        super().grid(
            row = row, # Número da linha.
            column = column, # Número da coluna.
            padx = kwargs.pop("padx", styles.PADDING_MEDIUM),
            pady = kwargs.pop("pady", styles.PADDING_MEDIUM),
            **kwargs # Parâmetros extras.
        )
