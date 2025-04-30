"""
Componente de Label para o título de um menu, já possuindo as seguintes customizações:
    - Fonte customizada.
    - Espaçamento externo.
"""

import ttkbootstrap as ttk

import source.styles as styles


class TitleLabel(ttk.Label):

    parent = None # Janela pai.

    # Método construtor.
    # ├─ parent: janela pai.
    # ├─ text: texto para exibir no Label.
    # └─ **kwargs: parâmetros extras.
    def __init__(self, parent, text:str, **kwargs)->None:

        self.parent = parent

        # Constrói o Label.
        super().__init__(
            self.parent, # Janela pai.
            text = text, # Texto do Label.
            font = kwargs.pop("font", (styles.FONT, styles.FONT_SIZE_LARGE, "bold")), # Configurações de fonte.
            anchor = kwargs.pop("anchor", "center"), # Alinhamento do texto.
            **kwargs # Parâmetros extras.
        )
    
    # Sobrescreve o método "pack()" da super classe.
    # └─ **kwargs: parâmetros extras.
    def pack(self, **kwargs)->None:
        super().pack(
            fill = kwargs.pop("fill", "x"), # Preenchimento.
            padx = kwargs.pop("padx", 0), # Espaçamento externo x.
            pady = kwargs.pop("pady", styles.PADDING_LARGE), # Espaçamento externo y.
            **kwargs # Parâmetros extras.
        )
    
    # Sobrescreve o método "grid()" da super classe.
    # ├─ row: número da linha.
    # ├─ column: número da coluna.
    # └─ **kwargs: parâmetros extras.
    def grid(self, row:int, column:int, **kwargs)->None:
        super().grid(
            row = row, # Número da linha.
            column = column, # Número da coluna.
            sticky = kwargs.pop("sticky", "ew"), # Posição e preenchimento na célula.
            padx = kwargs.pop("padx", 0), # Espaçamento externo x.
            pady = kwargs.pop("pady", styles.PADDING_LARGE), # Espaçamento externo y.
            **kwargs # Parâmetros extras.
        )