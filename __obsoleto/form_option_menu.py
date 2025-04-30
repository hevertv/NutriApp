"""
Componente de um OptionMenu para formulários. Possui as seguintes formatações:
    - 
"""

import tkinter as tk
import tkinter.font as tk_font
from typing import List

import source.styles as styles

class FormOptionMenu(tk.OptionMenu):

    parent = None # Janela pai.
    selected_value:tk.StringVar # Armazena o valor selecionado.
    default_value:str = "Selecione..." # Valor exibido antes do usuário expandir a lista.

    # Método construtor.
    def __init__(self, parent, values:List[str])->None:

        self.parent = parent
        values = [self.default_value] + values # Insere este valor para exibir ao usuário enquanto ele não selecionar qualquer valor.

        # Define o valor selecionado.
        self.selected_value = tk.StringVar(value = values[0])

        super().__init__(
            self.parent, # Janela pai.
            self.selected_value, # Define a variável para armazenar o valor selecionado.
            *values[1:], # Cria a lista de valores, desconsiderando a opção 0.
        )

        # Estiliza este componente.
        self.configure(
            activebackground = styles.COLOR_FOREGROUND, # Cor de fundo quando passar o mouse em cima.
            activeforeground = styles.COLOR_FONT_DARK, # Cor do texto quando passar o mouse em cima.
            anchor = "w", # Posição do texto selecionado.
            background = styles.COLOR_INPUT, # Cor de fundo padrão.
            borderwidth = 0, # Tamanho da borda externa.
            cursor = "hand2", # Ícone do mouse ao passar o mouse em cima.
            foreground = styles.COLOR_FONT_DARK, # Cor do texto padrão.
            font = tk_font.Font(family = styles.FONT, size = styles.FONT_SIZE_MEDIUM), # Configurações de fonte.
            highlightbackground = styles.COLOR_BORDER, # Cor da borda interna.
            highlightthickness = 1, # Tamanho da borda interna.
            padx = styles.PADDING_MEDIUM, # Espaçamento interno x.
            pady = 1, # Espaçamento interno y.
            width = 15 # Largura do componente.
        )

    def pack(self, **kwargs)->None:
        super().pack(
            padx = 0,
            pady = 0,
            **kwargs
        )

    def grid(self, row:int, column:int, **kwargs)->None:
        super().grid(
            row = row,
            column = column,
            padx = 4,
            pady = 4,
            sticky = "nw",
            **kwargs
        )
    
    def get(self)->str:
        value = self.selected_value.get()
        if value == self.default_value:
            value = ""
        return value