"""
Componente de Text (textarea) para fomrulários, já possuindo as seguintes customizações:
    - Altura e largura.
    - Fonte customizada.
    - Espaçamento externo.
"""

import ttkbootstrap as ttk

import source.styles as styles

class FormText(ttk.Text):

    parent = None # Janela pai.

    # Método construtor.
    # ├─ parent: janela pai.
    # ├─ height (opcional): altura do componente em linhas.
    # ├─ width (opcional): largura do componente em colunas.
    # └─ **kwargs: parâmetros extras.
    def __init__(self, parent, height:int = 3, width = 20, **kwargs)->None:

        self.parent = parent

        # Constrói o Text.
        super().__init__(
            self.parent, # Janela pai.
            height = height, # Altura do componente.
            width = width, # Largura do componente.
            font = kwargs.pop("font", (styles.FONT, styles.FONT_SIZE_MEDIUM)), # Configurações de fonte.
            **kwargs # Parâmetros extras.
        )

    # Sobrescreve o método "pack()" da super classe.
    # └─ **kwargs: parâmetros extras.
    def pack(self, **kwargs)->None:
        super().pack(
            fill = kwargs.pop("fill", "x"), # Preenchimento.
            padx = kwargs.pop("padx", styles.PADDING_SMALL), # Espaçamento externo x.
            pady = kwargs.pop("pady", (0, styles.PADDING_LARGE - 2)), # Espaçamento externo y.
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
            padx = kwargs.pop("padx", styles.PADDING_SMALL), # Espaçamento externo x.
            pady = kwargs.pop("pady", (styles.PADDING_SMALL, styles.PADDING_LARGE - 2)), # Espaçamento externo y.
            **kwargs # Parâmetros extras.
        )
    
    # Obtém o valor digitado no componente.
    def get(self)->str:
        return super().get("1.0", "end-1c") # Obtém do primeiro caracter até o último.
