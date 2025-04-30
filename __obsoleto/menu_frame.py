"""
Componente para criar um menu com todas as suas configurações.
Nota: para que seja possível criar um scrollbar, foi montada a seguinte estrutura:
    parent -> frame_outer -> (scrollbar, canvas) -> MenuFrame
    1. parent: o widget pai de todo o componente.
    2. frame_outer: frame para comportar todos os elementos do componente, posicionado no parent.
    3. scrollbar: scroll para a tela, posicionado no frame_outer.
    4. canvas: espaço para ser possível colocar o scrollbar, posicionado no frame_outer.
    5. MenuFrame: o próprio componente, posicionado no canvas.
"""

import ttkbootstrap as ttk

import source.styles as styles


class MenuFrame(ttk.Frame):

    parent = None # Janela pai.
    open_menu = None # Método de referência para navegar entre os menus.
    frame_outer:ttk.Frame = None # Frame externo para comportar todos os elementos do componente.
    scrollbar:ttk.Scrollbar = None # Scroll para o menu.
    canvas:ttk.Canvas = None # Canvas para posicionar o scrollbar.
    window_to_canvas = None # Janela interna do canvas para possibilitar a estrutura.

    # Método construtor.
    # ├─ parent: janela pai.
    # ├─ open_menu: método de referência para navegar entre os menus.
    # └─ **kwargs: parâmetros extras para o Frame do menu.
    def __init__(self, parent, open_menu, **kwargs)->None:

        self.parent = parent
        self.open_menu = open_menu

        # Constrói todos os elementos do componente.
        #   parent -> frame_outer -> (scrollbar, canvas) -> self
        self.frame_outer = ttk.Frame(self.parent)
        self.scrollbar = ttk.Scrollbar(self.frame_outer, orient = "vertical")
        self.scrollbar.pack(fill = "y", side = "right", expand = False)
        self.canvas = ttk.Canvas(self.frame_outer, yscrollcommand = self.scrollbar.set)
        self.canvas.pack(side = "left", fill = "both", expand = True)
        self.scrollbar.config(command = self.canvas.yview)

        # Reseta a visualização para criar o scroll corretamente.
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

        # Finaliza criando o frame interno (self).
        super().__init__(
            self.canvas, # Janela pai.
            **kwargs # Parâmetros extras.
        )

        # Cria uma janela interna do canvas para possibilitar toda a estrutura.
        self.window_to_canvas:int = self.canvas.create_window(0, 0, window = self, anchor = "nw")

        # Configura para chamar os métodos abaixo quando houver alguma alteração no tamanho da janela.
        self.bind("<Configure>", self.__configure_interior) # Para o frame interno (self).
        self.bind("<Configure>", self.__configure_canvas) # Para o canvas.
    

    # Método para sincronizar o scroll de acordo com o tamanho do frame interno (self) e o que estiver dentro dele.
    # └─ __event: parâmetro necessário apenas para não gerar erro, mas não é utilizado.
    def __configure_interior(self, __event)->None:

        # Obtém o tamanho do frame interno (self).
        size = (self.winfo_reqwidth(), self.winfo_reqheight())

        # Configura o scroll do canvas.
        self.canvas.config(scrollregion = "0 0 %s %s" % size)

        # Atualiza a largura do canvas.
        if self.winfo_reqwidth() != self.canvas.winfo_width():
            self.canvas.config(width = self.winfo_reqwidth())
    

    # Método para sincronizar o canvas de acordo com o tamanho do frame interno (self) e o que estiver dentro dele.
    # └─ __event: parâmetro necessário apenas para não gerar erro, mas não é utilizado.
    def __configure_canvas(self, __event)->None:

        # Atualiza o frame interno (self) para preencher o canvas.
        if self.winfo_reqwidth() != self.canvas.winfo_width():
            self.canvas.itemconfigure(self.window_to_canvas, width = self.canvas.winfo_width())
        
    
    # Sobrescreve o método "pack()" da super classe.
    # └─ **kwargs: parâmetros extras.
    def pack(self, **kwargs)->None:
        self.frame_outer.pack(
            fill = "both",
            expand = True
        )
        super().pack(
            fill = kwargs.pop("fill", "both"),
            expand = kwargs.pop("expand", True),
            **kwargs # Parâmetros extras.
        )

    # Sobrescreve o método "destroy()" da super classe.
    def destroy(self):
        super().destroy()
        self.frame_outer.destroy()