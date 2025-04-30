"""
Componente de Button já possuindo as seguintes customizações:
    - Cursor exibido ao passar o mouse em cima.
    - Espaçamento externo.
"""

import ttkbootstrap as ttk

import source.styles as styles


class ModelButton(ttk.Button):

    parent = None # Janela pai.
    
    # Método construtor.
    # ├─ parent: janela pai.
    # ├─ text: texto exibido no botão.
    # ├─ bootstyle (opcional): estilo bootstrap do botão.
    # └─ **kwargs: parâmetros extras.
    def __init__(self, parent, text:str, bootstyle:str = "primary", **kwargs)->None:

        self.parent = parent

        # Constrói o Button.
        super().__init__(
            self.parent, # Janela pai.
            text = text, # Texto exibido.
            cursor = kwargs.pop("cursor", "hand2"), # Ponteiro do mouse ao passar em cima do Button.
            bootstyle = kwargs.pop("bootstyle", bootstyle), # Estilo bootstrap do botão.
            **kwargs # Parâmetros extras.
        )

    # Sobrescreve o método "pack()" da super classe.
    # └─ **kwargs: parâmetros extras.
    def pack(self, **kwargs)->None:
        super().pack(
            padx = kwargs.pop("padx", styles.PADDING_SMALL), # Espaçamento externo x.
            pady = kwargs.pop("pady", 0), # Espaçament externo y.
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
            sticky = kwargs.pop("sticky", "n"), # Gruda o botão no topo.
            padx = kwargs.pop("padx", styles.PADDING_SMALL), # Espaçamento externo x.
            pady = kwargs.pop("pady", 0), # Espaçamento externo y.
            **kwargs # Parâmetros extras.
        )