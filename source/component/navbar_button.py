"""
Componente de Button com uso exclusivo da Navbar já possuindo as seguintes customizações:
    - Alteração entre o estilo ao estar selecionado ou não selecionado.
    - Ícone sendo exibido no botão.
"""

import ttkbootstrap as ttk

import source.styles as styles


class NavbarButton(ttk.Button):

    parent = None # Janela pai.
    icon:ttk.PhotoImage = None # Ícone exibido no botão quando não está selecionado.
    icon_when_selected:ttk.PhotoImage # Ícone exibido no botão quando está selecionado.

    _selected:bool = False # Atributo para alterar a estilização do botão entre selecionado e não selecionado.

    # Getter de "_selected".
    @property
    def selected(self)->bool:
        return self._selected

    @selected.setter
    def selected(self, new_value:bool)->None:
        self._selected = new_value

        # Botão selecionado.
        if self._selected:
            self.configure(bootstyle="primary", image = self.icon_when_selected)
        
        # Botão não selecionado.
        else:
            self.configure(bootstyle="light", image = self.icon)
    

    # Método construtor.
    # ├─ parent: janela pai.
    # ├─ text: texto exibido no botão.
    # ├─ path_icon (opcional): caminho na pasta para carregar o ícone quando o botão não está selecionado.
    # ├─ path_icon_when_selected (opcional): caminho na pasta para carregar o ícone quando o botão está selecionado.
    # └─ **kwargs: parâmetros extras.
    def __init__(self, parent, text:str, path_icon:str = "", path_icon_when_selected:str = "", **kwargs)->None:

        self.parent = parent

        # Carrega os ícones (divide o tamanho original por 4, para ficar 16x16 pixels).
        self.icon = ttk.PhotoImage(file = path_icon).subsample(4)
        self.icon_when_selected = ttk.PhotoImage(file = path_icon_when_selected).subsample(4)

        # Constrói o Button.
        super().__init__(
            self.parent,
            text = text, # Texto exibido.
            compound = kwargs.pop("compound", "left"), # Ícone é exibido na esquerda do texto.
            cursor = kwargs.pop("cursor", "hand2"), # Cursor ao passar o mouse em cima.
            **kwargs # Parâmetros extras.
        )

        self.selected = False
    
    # Sobrescreve o método "pack()" da super classe.
    # └─ **kwargs: parâmetros extras.
    def pack(self, **kwargs)->None:
        super().pack(
            fill = kwargs.pop("fill", "x"), # Preenche todo o espaço na horizontal disponível.
            **kwargs
        )

