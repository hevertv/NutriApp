"""
Barra lateral de navegação entre os menus.
"""

import ttkbootstrap as ttk
import os

import source.styles as styles
from source.component.navbar_button import NavbarButton

PATH_GROUP = "source/image/group_light.png"
PATH_GROUP_PRIMARY = "source/image/group_primary.png"
PATH_CALENDAR = "source/image/calendar_light.png"
PATH_CALENDAR_PRIMARY = "source/image/calendar_primary.png"
PATH_GLOBE = "source/image/globe_light.png"
PATH_GLOBE_PRIMARY = "source/image/globe_primary.png"
PATH_SETTINGS = "source/image/settings_light.png"
PATH_SETTINGS_PRIMARY = "source/image/settings_primary.png"
PATH_LOGOUT = "source/image/logout_light.png"
PATH_LOGOUT_PRIMARY = "source/image/logout_primary.png"
PATH_USER_DATA = "data/user_data.json" # Caminho do arquivo que armazena o login/senha do usuário.


class Navbar(ttk.Frame):

    parent = None # Janela pai.
    open_menu = None # Armazena o método para abrir os menus ao clicar nos botões.
    button_selected:NavbarButton = None # Armazena o botão ativo no momento.

    first_invoke:bool = True # Apenas uma gambiarra para clicar em um botão ao carregar a Navbar.

    # Método construtor.
    # ├─ parent: janela pai.
    # └─ open_menu: método para abrir os menus ao clicar nos botões.
    def __init__(self, parent, open_menu)->None:

        self.parent = parent
        self.open_menu = open_menu

        # Constrói a Navbar.
        super().__init__(self.parent, width = 180, bootstyle = "light")
        self.pack()

        # Logo no topo.
        label_logo = ttk.Label(self, text = "NutriApp", bootstyle = "light-inverse", font = (styles.FONT_LOGOTYPE, styles.FONT_SIZE_INTERMEDIATE, "bold"), padding = (0, styles.PADDING_MEDIUM))
        label_logo.pack()

        # Criação dos botões.
        button_paciente_lista = NavbarButton(
            self,
            text = "Pacientes",
            path_icon = PATH_GROUP_PRIMARY,
            path_icon_when_selected = PATH_GROUP,
            command = lambda: self.__open_menu(button_paciente_lista, "paciente_lista")
        )
        button_paciente_lista.pack()
        
        button_agenda = NavbarButton(
            self,
            text = "Agenda",
            path_icon = PATH_CALENDAR_PRIMARY,
            path_icon_when_selected = PATH_CALENDAR,
            command = lambda: self.__open_menu(button_agenda, "agenda")
        )
        button_agenda.pack()

        # Botão de notícias.
        button_noticias = NavbarButton(
            self,
            text = "Notícias",
            path_icon = PATH_GLOBE_PRIMARY,
            path_icon_when_selected = PATH_GLOBE,
            command = lambda: self.__open_menu(button_noticias, "noticias")
        )
        button_noticias.pack()

        # Botão de configurações.
        button_configuracoes = NavbarButton(
            self,
            text = "Configurações",
            path_icon = PATH_SETTINGS_PRIMARY,
            path_icon_when_selected = PATH_SETTINGS,
            command = lambda: self.__open_menu(button_configuracoes, "configuracoes")
        )
        button_configuracoes.pack()

        # Botão de sair.
        button_sair = NavbarButton(
            self,
            text = "Sair",
            path_icon = PATH_LOGOUT_PRIMARY,
            path_icon_when_selected = PATH_LOGOUT,
            command = lambda: (
                self.__logout(),
                self.open_menu("login")
            )
        )
        button_sair.pack(side = "bottom") # Posiciona na parte inferior da janela.

        # Gambiarra para manter um botão selecionado quando carregar a Navbar no projeto.
        button_paciente_lista.invoke()
        self.first_invoke = False
    
    
    # Método para dar o efeito de botão selecionado.
    # ├─ navbar_button: botão da navbar para criar o efeito de selecionado.
    # └─ menu_name: nome do menu para abrir no App.
    def __open_menu(self, navbar_button:NavbarButton, menu_name:str)->None:

        # Remove a seleção do botão que estava selecionado.
        if self.button_selected:
            self.button_selected.selected = False
        
        # Seleciona o novo botão (isso altera seu layout) e armazena essa informação.
        self.button_selected = navbar_button
        self.button_selected.selected = True

        # Apenas uma gambiarra para quando a navbar carregar no projeto, não abrir 2x o menu.
        if not self.first_invoke:
            self.open_menu(menu_name)

    
    def __logout(self)->None:
        
        try:
            os.remove(PATH_USER_DATA)
        except OSError as error:
            print(f"Erro ao excluir o arquivo. {error}")
       
