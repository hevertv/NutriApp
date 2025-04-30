"""
Componente de Label para formulários, já possuindo as seguintes customizações:
    - Alinhamento do texto.
    - Fonte customizada.
    - Espaçamento externo.
"""

import ttkbootstrap as ttk

import source.styles as styles

class FormLabel(ttk.Label):

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
            anchor = kwargs.pop("anchor", "w"), # Alinhamento do texto.
            font = kwargs.pop("font", (styles.FONT, styles.FONT_SIZE_MEDIUM)), # Configurações de fonte.
            **kwargs # Parâmetros extras.
        )
    
    # Sobrescreve o método "pack()" da super classe.
    # └─ **kwargs: parâmetros extras.
    def pack(self, **kwargs)->None:
        super().pack(
            fill = kwargs.pop("fill", "x"), # Preenchimento.
            padx = kwargs.pop("padx", styles.PADDING_SMALL), # Espaçamento externo x.
            pady = kwargs.pop("pady", (styles.PADDING_SMALL, 0)), # Espaçamento externo y.
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
            sticky = kwargs.pop("sticky", "new"), # Posição e preenchimento na célula.
            padx = kwargs.pop("padx", (styles.PADDING_SMALL, styles.PADDING_MEDIUM)), # Espaçamento externo x.
            pady = kwargs.pop("pady", 0), # Espaçamento externo y.
            **kwargs # Parâmetros extras.
        )
