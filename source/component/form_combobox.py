"""
Componente de Combobox (dropdown) para formulários, já possuindo as seguintes customizações:
    - Texto default informando que o usuário deve escolher uma opção.
    - Input de novos valores desabilitados.
    - Cursor alterado ao passar o mouse em cima.
    - Fonte customizada.
    - Espaçamento externo.
"""

import ttkbootstrap as ttk
from typing import List

import source.styles as styles

class FormCombobox(ttk.Combobox):

    parent = None # Janela pai.
    default_value:str = "Selecione..." # Valor exibido antes do usuário expandir a lista.
    selected_value:ttk.StringVar = None # Armazena o valor selecionado.

    # Método construtor.
    # ├─ parent: janela pai.
    # ├─ values: lista com os valores para o usuário selecionar.
    # ├─ width (opcional): largura do componente.
    # └─ **kwargs: parâmetros extras.
    def __init__(self, parent, values:List[str], width = 18, **kwargs)->None:

        self.parent = parent
        self.selected_value = ttk.StringVar(value = self.default_value) # Armazena o valor selecionado como "default".

        # Constrói o Combobox.
        super().__init__(
            self.parent, # Janela pai.
            values = values, # Lista de valores para o usuário selecionar.
            width = width, # Largura do componente.
            textvariable = kwargs.pop("textvariable", self.selected_value), # Armazena o valor selecionado pelo usuário.
            state = kwargs.pop("state", "readonly"), # Desabilita a entrada de novos valores.
            cursor = kwargs.pop("cursor", "hand2"), # Ponteiro do mouse ao passar em cima do componente.
            font = kwargs.pop("font", (styles.FONT, styles.FONT_SIZE_MEDIUM)), # Configurações de fonte.
            **kwargs # Parâmetros extras.
        )
    
    # Sobrescreve o método "pack()" da super classe.
    # └─ **kwargs: parâmetros extras.
    def pack(self, **kwargs)->None:
        super().pack(
            fill = kwargs.pop("fill", "x"), # Preenchimento.
            padx = kwargs.pop("padx", styles.PADDING_SMALL), # Espaçamento interno x.
            pady = kwargs.pop("pady", (0, styles.PADDING_LARGE - 2)), # Espaçamento interno y.
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
            pady = kwargs.pop("pady", (styles.PADDING_SMALL-1, styles.PADDING_LARGE)), # Espaçamento externo y.
            **kwargs # Parâmetros extras.
        )

    # Método para obter o valor selecionado no componente.
    def get(self)->str:

        # Se o usuário ainda não tiver selecionado nada, irá retornar "".
        value = self.selected_value.get()
        if value == self.default_value:
            value = ""
        return value
