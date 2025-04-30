"""
Arquivo para armazenar constantes para a estilização do projeto.
    - Cores.
    - Fontes.
    - Espaçamentos.
Nota: a classe Styles é utilizada somente para carregar algumas configurações extras ao rodar o projeto na main.
"""

import ttkbootstrap as ttk

# Cores do projeto.
COLOR_BORDER = "#DEE2E6"
COLOR_BACKGROUND = "#EBEBEB"
COLOR_FOREGROUND = "#F8F9FA"
COLOR_INPUT = "#FFFFFF"

COLOR_FONT_DARK = "#232323"
COLOR_FONT_DISABLED = "#686A6D"
COLOR_FONT_LIGHT = "#FFFFFF"

COLOR_PRIMARY = "#0D6EFD"
COLOR_PRIMARY_DISABLED = "#5F9EFB"

COLOR_SECONDARY = "#6C757D"
COLOR_SECONDARY_DISABLED = "#9DA3A8"

COLOR_SUCCESS = "#28A745"
COLOR_SUCCESS_DISABLED = "#4FAA6F"

COLOR_WARNING = "#FFC107"
COLOR_WARNING_DISABLED = "#F8D057"

COLOR_DANGER = "#DC3545"
COLOR_DANGAR_DISABLED = "#E1757F"

# Opções de fonte.
FONT = "Arial"
FONT_LOGOTYPE = "Sitka Small"
FONT_SIZE_SMALL = 8
FONT_SIZE_MEDIUM = 12
FONT_SIZE_INTERMEDIATE = 24
FONT_SIZE_LARGE = 36
FONT_SIZE_GIANT = 72

# Espaçamento entre os objetos.
PADDING_SMALL = 4
PADDING_MEDIUM = 12
PADDING_LARGE = 20


# Classe para atualizar alguns estilos do bootstrap no projeto.
class Styles():

    # Método construtor.
    def __init__(self)->None:
        
        # Chama o método para atualizar a fonte dos botões bootstrap.
        self.__update_button_font()
    
    # Método para atualizar a fonte dos botões bootstrap (o original é muito pequeno).
    def __update_button_font(self)->None:

        # Cria um loop para passar dentro de todos os temas do bootstrap.
        for theme in ["", "primary", "secondary", "success", "info", "warning", "danger"]:
            style = theme
            if style != "":
                style += "."
            
            # Cria outro loop para passar dentro de todos os estilos do bootstrap.
            for type in ["", "Outline", "Link"]:
                final_style = style + type
                if type != "":
                    final_style += "."
                final_style += "TButton"
                
                # Ao final, atualiza o tamanho da fonte.
                ttk.Style().configure(final_style, font = (FONT, FONT_SIZE_SMALL if final_style.startswith("info") else FONT_SIZE_MEDIUM))
