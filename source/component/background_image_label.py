"""
Componente de Label com uma imagem para ser utilizado como plano de fundo.
"""

import ttkbootstrap as ttk
from PIL import ImageTk


class BackgroundImageLabel(ttk.Label):

    parent = None # Janela pai.
    image:ttk.Image = None # Armazena a imagem original, apenas em memória.
    image_background:ttk.Image = None # Armazena a imagem redimensionada que é exibida ao usuário.
    image_ratio:float = None # Armazena a proporção do tamanho da imagem (width / height).

    # Método construtor.
    # ├─ parent: janela pai.
    # └─ path_image: caminho para carregar a imagem e exibir como plano de fundo.
    def __init__(self, parent, path_image:str)->None:

        self.parent = parent

        # Carrega a imagem de fundo e calcula sua proporção.
        self.image = ttk.Image.open(path_image)
        self.image_ratio = self.image.width / self.image.height

        # Transforma a imagem para ser exibida corretamente.
        self.image_background = ImageTk.PhotoImage(self.image)

        # Cria o Label para exibir a imagem.
        super().__init__(
            parent, # Janela pai.
            image = self.image_background # Imagem exibida.
        )
        # Detecta quando a janela pai tiver seu tamanho alterado.
        parent.bind("<Configure>", self.__resize_image)
    

    # Método para redimensionar a imagem quando o tamanho da janela pai for alterado.
    # └─ event: valor recebido do "bind" para obter o novo tamanho da janela. 
    def __resize_image(self, event)->None:
        
        # Calcula a nova proporção da janela.
        window_ratio = event.width / event.height

        # Redimensiona a exibição da imagem de acordo com os novos valores.
        if window_ratio > self.image_ratio:
            self.image_background = ImageTk.PhotoImage(self.image.resize((event.width, int(event.width / 1.5))))
        else:
            self.image_background = ImageTk.PhotoImage(self.image.resize((int(event.height * 1.5), event.height)))

        # Exibe a imagem redimensionada.
        self.configure(image = self.image_background)


    # Sobrescreve o método "place()" da super classe.
    def place(self, **kwargs)->None:

        super().place(
            relx = kwargs.pop("relx", 0.5),
            rely = kwargs.pop("rely", 0.5),
            anchor = kwargs.pop("anchor", "center")
        )






