"""
Menu para exibir a agenda do nutricionista.
"""

import ttkbootstrap as ttk

from source.banco_dados import BancoDados
from source.component.background_image_label import BackgroundImageLabel


PATH_BACKGROUND = "source/image/agenda_background.png"


class MenuAgenda(ttk.Frame):

    parent = None # Janela pai.
    open_menu = None # Método de referência para alterar de menu.
    banco_dados:BancoDados = None # Conexão com o banco de dados.

    # Método construtor.
    # ├─ parent: janela pai.
    # ├─ open_menu: método de referência para alterar de menu.
    # └─ banco_dados: conexão com o banco de dados.
    def __init__(self, parent, open_menu, banco_dados:BancoDados)->None:

        self.parent = parent
        self.open_menu = open_menu
        self.banco_dados = banco_dados

        # Constrói o menu.
        super().__init__(parent)
        self.pack()

        # Cria a imagem de fundo.
        menu_background = BackgroundImageLabel(self, PATH_BACKGROUND)
        menu_background.place()
