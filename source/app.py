"""
Arquivo que mantêm a navegação entre os menus do aplicativo.
"""

import ttkbootstrap as ttk

from source.banco_dados import BancoDados
from source.navbar import Navbar
from source.menu.menu_agenda import MenuAgenda
from source.menu.menu_anamnese import MenuAnamnese
from source.menu.menu_antropometria import MenuAntropometria
from source.menu.menu_configuracoes import MenuConfiguracoes
from source.menu.menu_inquerito_alimentar import MenuInqueritoAlimentar
from source.menu.menu_login import MenuLogin
from source.menu.menu_noticias import MenuNoticias
from source.menu.menu_nutricionista import MenuNutricionista
from source.menu.menu_paciente_lista import MenuPacienteLista
from source.menu.menu_paciente import MenuPaciente
from source.menu.menu_perfil_nutricional import MenuPerfilNutricional


class App(ttk.Frame):

    parent = None # Janela pai.
    paned_window:ttk.PanedWindow = None # Widget que cria a divisão de tela (navbar/menu).
    navbar:Navbar = None # Barra de navegação.
    menu_opened = None # Menu aberto atualmente.
    menu_opened_name = "" # Nome do menu aberto atualmente.
    banco_dados = None # Conexão com banco de dados.


    # Método construtor.
    # └─ parent: janela pai.
    def __init__(self, parent)->None:

        self.parent = parent

        # Constrói o Frame do App.
        super().__init__(self.parent)
        self.pack(fill = "both", expand = True)

        # Inicia a conexão com o banco de dados.
        self.banco_dados = BancoDados()

        # Ao inicializar, abre o MenuLogin.
        self.__open_menu("login")


    # Método que cria a divisão de tela.
    def __create_app(self)->None:

        # Divisão de tela.
        self.paned_window = ttk.PanedWindow(
            self, # Janela pai.
            orient = "horizontal", # Divisão na horizontal (navbar | menu).
        )
        self.paned_window.pack(
            fill = "both", # Ocupa todo o espaço disponível.
            expand = True # Preenche todo o espaço disponível.
        )

        # Navbar.
        self.navbar = Navbar(
            self.paned_window, # Janela pai.
            open_menu = lambda menu_name: self.__open_menu(menu_name) # Método para abrir o menu ao clicar nos botões da navbar.
        )

        # Adiciona a navbar na divisão de tela.
        self.paned_window.add(self.navbar)


    # Método para abrir um determinado menu.
    # └─ menu_name: string recebida para decidir qual menu abrir.
    def __open_menu(self, menu_name)->None:
        
        # Se o menu para abrir está aberto atualmente, saia sem fazer nada.
        if self.menu_opened_name == menu_name:
            return

        self.menu_opened_name = menu_name

        # Deleta o menu que está aberto antes de adicionar outro.
        if self.menu_opened:
            self.menu_opened.destroy()
            self.menu_opened = None
        
        # Para abrir o MenuLogin ou MenuNutricionista, a navbar não deve existir, então ela é deletada (caso exista).
        if menu_name == "login" or menu_name == "nutricionista":
            if self.paned_window:
                self.paned_window.destroy()
                self.paned_window = None
            match menu_name:
                case "login": self.menu_opened = MenuLogin(self, self.__open_menu, self.banco_dados)
                case "nutricionista": self.menu_opened = MenuNutricionista(self, self.__open_menu, self.banco_dados)
            return

        # Em outros menus, criar a navbar junto com a divisão de tela (caso ainda não tenha sido criada).
        if self.paned_window is None:
            self.__create_app()
        
        # Escolhe qual menu abrir.
        match menu_name:

            case "agenda": self.menu_opened = MenuAgenda(self.paned_window, self.__open_menu, self.banco_dados)
            case "anamnese": self.menu_opened = MenuAnamnese(self.paned_window, self.__open_menu, self.banco_dados)
            case "antropometria": self.menu_opened = MenuAntropometria(self.paned_window, self.__open_menu, self.banco_dados)
            case "configuracoes": self.menu_opened = MenuConfiguracoes(self.paned_window, self.__open_menu, self.banco_dados)
            case "inquerito_alimentar": self.menu_opened = MenuInqueritoAlimentar(self.paned_window, self.__open_menu, self.banco_dados)
            case "noticias": self.menu_opened = MenuNoticias(self.paned_window, self.__open_menu, self.banco_dados)
            case "paciente": self.menu_opened = MenuPaciente(self.paned_window, self.__open_menu, self.banco_dados)
            case "paciente_lista": self.menu_opened = MenuPacienteLista(self.paned_window, self.__open_menu, self.banco_dados)
            case "perfil_nutricional": self.menu_opened = MenuPerfilNutricional(self.paned_window, self.__open_menu, self.banco_dados)

            # Nenhum caso anterior (para erro de digitação de quem programou).
            case _:
                raise Exception("Menu desconhecido para abrí-lo. Valor recebido:", menu_name)

        self.paned_window.add(self.menu_opened)
