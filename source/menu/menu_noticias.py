"""
Menu para exibir as últimas notícias.
"""

import ttkbootstrap as ttk

from source.banco_dados import BancoDados
from source.component.background_image_label import BackgroundImageLabel
from source.component.title_label import TitleLabel


PATH_BACKGROUND = "source/image/noticias_background.png"


class MenuNoticias(ttk.Frame):

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

        # Cria o título do menu.
        title = TitleLabel(self, text = "Notícias")
        title.pack(pady = 0)