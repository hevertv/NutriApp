"""
Componente de Frame com um scrollbar quando as informações internas forem maiores que o tamanho da tela.
Nota: para que seja possível criar o Frame, é montada a seguinte estrutura hierárquica:
    parent -> frame_outer -> (scrollbar, canvas) -> self
    1. parent: o widget pai de todo o componente.
    2. frame_outer: um Frame para comportar todos os elementos do componente, posicionado dentro do parent.
    3. scrollbar: o scroll para a tela, posicionado dentro do frame_outer.
    4. canvas: um espaço para ser possível colocar o scrollbar, posicionado dentro do frame_outer.
    5. self: o próprio componente do tipo Frame, posicionado dentro do canvas
"""


import ttkbootstrap as ttk


class ScrollbarFrame(ttk.Frame):

    parent = None # Janela pai.
    frame_outer:ttk.Frame = None # É o frame externo, que comporta o canvas, scrollbar e o frame interno.

    # Método construtor.
    # ├─ parent: janela pai.
    # └─ **kwargs: parâmetros extras para o Frame externo.
    def __init__(self, parent, **kwargs)->None:
        
        self.parent = parent

        # Constrói todos os elementos do componente na seguinte estrutura hierárquica:
        #   parent -> frame_outer -> (scrollbar, canvas) -> self
        self.frame_outer = ttk.Frame(self.parent, padding = 64, bootstyle = "danger")
        scrollbar = ttk.Scrollbar(self.frame_outer, orient = "vertical")
        scrollbar.pack(fill = "y", side = "right", expand = False)
        self.canvas = ttk.Canvas(self.frame_outer, yscrollcommand = scrollbar.set) # bd = 0, # highlightthickness = 0,
        self.canvas.pack(side = "left", fill = "both", expand = True)
        scrollbar.config(command = self.canvas.yview)

        # Reseta a visualização para criar o scroll corretamente.
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

        # Finaliza criando o Frame interno (self).
        super().__init__(self.canvas)
        self.window_to_canvas = self.canvas.create_window(0, 0, window = self, anchor = "nw") # Cria uma janela interna do canvas para possibilitar toda a estrutura.

        # Configura para chamar os métodos abaixo quando houver alguma alteração no tamanho da janela.
        self.bind("<Configure>", self.__configure_interior) # Para o Frame interno (self).
        self.canvas.bind("<Configure>", self.__configure_canvas) # Para o canvas.


    # Método para sincronizar o scroll de acordo com o tamanho do Frame interno (self) e o que estiver dentro dele.
    # └─ __event: parâmetro necessário apenas para não gerar erro, mas não é utilizado.
    def __configure_interior(self, __event)->None:

        # Obtém o tamanho do Frame interno (self).
        size = (self.winfo_reqwidth(), self.winfo_reqheight())

        # Configura o scroll do canvas.
        self.canvas.config(scrollregion = "0 0 %s %s" % size)

        # Atualiza a largura do canvas.
        if self.winfo_reqwidth() != self.canvas.winfo_width():
            self.canvas.config(width = self.winfo_reqwidth())


    # Método para sincronizar o canvas de acordo com o tamanho do Frame interno (self) e o que estiver dentro dele.
    # └─ __event: parâmetro necessário apenas para não gerar erro, mas não é utilizado.
    def __configure_canvas(self, __event)->None:

        # Atualiza o Frame interno (self) para preencher o canvas.
        if self.winfo_reqwidth() != self.canvas.winfo_width():
            self.canvas.itemconfigure(self.window_to_canvas, width = self.canvas.winfo_width())


    # Método
    def pack(self, **kwargs)->None:
        self.frame_outer.pack(
            fill = "both",
            expand = True,
            **kwargs
        )
