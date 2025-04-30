"""
Componente de Frame com um scroll.
"""

import ttkbootstrap as ttk


class ScrollableFrame(ttk.Frame):

    parent = None # Janela pai.
    frame_outer:ttk.Frame = None # Frame externo para comportar todos os elementos do componente.
    scrollbar:ttk.Scrollbar = None # Scroll para o frame.
    canvas:ttk.Canvas = None # Canvas para posicionar o scrollbar.
    
    
    # Método construtor.
    # ├─ parent: janela pai.
    # └─ **kwargs: parâmetros extras.
    def __init__(self, parent, **kwargs)->None:

        self.parent = parent

        # Constrói todos os elementos do componente.
        #   parent -> frame_outer -> (scrollbar, canvas) -> self
        self.frame_outer = ttk.Frame(self.parent)
        self.scrollbar = ttk.Scrollbar(self.frame_outer, orient = "vertical")
        self.scrollbar.pack(fill = "y", side = "right", expand = False)
        self.canvas = ttk.Canvas(self.frame_outer, yscrollcommand = self.scrollbar.set, bd = 0, highlightthickness = 0, bg = "green")
        self.canvas.pack(side = "left", fill = "both", expand = True)
        self.scrollbar.config(command = self.canvas.yview)

        # Finaliza criando o frame interno.
        super().__init__(self.canvas, **kwargs)
        super().pack(fill = "both", expand = True)

        # Cria uma janela interna do canvas para possibilitar toda a estrutura.
        self.window = self.canvas.create_window((0, 0), window = self, anchor = "nw")
        
        # Configura para chamar os métodos abaixo quando houver alguma alteração na janela.
        self.canvas.bind("<Configure>", self.__configure_canvas)
        self.canvas.bind_all("<MouseWheel>", self.__on_mouse_wheel)

        self.__update_scrollbar()
    
    
    # Método para sincronizar o canvas de acordo com o tamanho da janela.
    # └─ __event: parâmetro necessário apenas para não gerar erro, mas neste caso não é utilizado.
    def __configure_canvas(self, __event)->None:
        self.canvas.configure(scrollregion = self.canvas.bbox("all"))
        self.__display_scroll()
        self.__update_scrollbar()


    # Método para detectar quando o usuário mover a "roletinha do mouse".
    def __on_mouse_wheel(self, event)->None:
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    
    
    # Método para exibir ou ocultar o scroll, de acordo com o tamanho da janela.
    def __display_scroll(self)->None:
        if self.canvas.winfo_height() < self.canvas.bbox("all")[3]:
            self.scrollbar.pack(side = "right", fill = "y")
        else:
            self.scrollbar.pack_forget()
    
    
    # Método para atualizar a posição do scrollbar.
    def __update_scrollbar(self)->None:
        self.canvas.update_idletasks()
        self.canvas.configure(scrollregion = self.canvas.bbox("all"), yscrollcommand = self.scrollbar.set)
        self.scrollbar.configure(command = self.canvas.yview)
        self.canvas.itemconfigure(self.window, width = self.canvas.winfo_width()) # Isto atualiza para que o self ocupe todo o espaço da tela.


    # Sobrescreve o método "pack()" da super classe.
    # └─ **kwargs: parâmetros extras.
    def pack(self, **kwargs)->None:
        self.frame_outer.pack(
            fill = kwargs.pop("fill", "both"),
            expand = kwargs.pop("expand", True),
            **kwargs # Parâmetros extras.
        )
    
    
    # Sobrescreve o método "grid()" da super classe.
    # └─ **kwargs: parâmetros extras.
    def grid(self, row:int, column:int, **kwargs)->None:
        self.frame_outer.grid(
            row = row,
            column = column,
            sticky = kwargs.pop("sticky", "nswe"),
            **kwargs # Parâmetros extras.
        )


    # Sobrescreve o método "destroy()" da super classe.
    def destroy(self):
        self.canvas.unbind_all("<MouseWheel>")
        super().destroy()
        self.frame_outer.destroy()