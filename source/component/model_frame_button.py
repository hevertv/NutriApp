"""

Componente de um Frame com as seguintes formatações pré-definidas:
    - Borda.
    - Cor de fundo.
    - Espaçamento interno e externo.

Como utilizar?
├─ 1. Importar a classe.
├─ 2. Inicializar o objeto.
└─ 3. Utilizar os métodos "pack()", "grid()" ou "place()" para exibí-lo.

Exemplo:
from source.component.frame_model import FrameModel
frame = FrameModel(parent)
frame.pack()

"""

# Importações de bibliotecas.
import tkinter as tk

# Importações do projeto.
import source.styles as styles

# Importações do componente
from source.component.model_frame import ModelFrame


# Classe do Frame com formatação pré-definida.
class ModelFrameButton(tk.Frame):

    # Armazena o "pai" deste componente.
    parent = None
    visible = False

    # Método construtor.
    # ├─ self: referência ao próprio objeto.
    # ├─ parent: janela "pai" para a inserção do componente.
    # └─ **kwargs: qualquer valor recebido neste método, desde que não seja outro parâmetro, será armazenado nesta variável (opcional).
    def __init__(self, 
                 parent,
                 text_to_button,
                 command = None,
                 **kwargs)->None:

        # Define que a variável seja o mesmo que o parâmetro recebido.
        self.parent = parent
         

        # Chama o construtor da super classe.
        super().__init__(
            self.parent, # Define a janela "pai".

            # borderwidth = kwargs.pop("borderwidth", 0), # Tamanho da borda padrão.
            # highlightthickness = kwargs.pop("highlightthickness", 1), # Tamanho da borda de destaque.
            # highlightbackground = kwargs.pop("highlightbackground", styles.COLOR_BORDER), # Cor da borda de destaque.
            # bg = kwargs.pop("bg", styles.COLOR_FOREGROUND), # Cor de fundo.

            # # Espaçamentos internos do componente
            # padx = kwargs.pop("padx", styles.PADDING_LARGE),
            # pady = kwargs.pop("pady", styles.PADDING_LARGE),

            # Define os parâmetros restantes que foram recebidos.
            **kwargs
        )

        button = tk.Button (
            self, 
            text = text_to_button, #text_to_button ==> Definir o titulo do botão
            command = command
        )
        button.pack(fill="x",expand=True)


        self.model_frame = ModelFrame(self)
    #self.model_frame.pack(fill="x",expand=True) 
    # ├─ No inicio da chamda do metodo, o expand vai inicar como TRUE e por isso todas abas estaram abertas


    # Método que sobrescreve o método "pack()" da super classe para que já possua certas customizações pré-definidas.
    # ├─ self: referência ao próprio objeto.
    # └─ **kwargs: qualquer valor recebido neste método, desde que não seja outro parâmetro, será armazenado nesta variável (opcional).
    def pack(self, **kwargs)->None:

        # Chama o método "pack()" da super classe para exibir o componente em seu "pai".
        super().pack(

            # Espaçamentos externos do componente.
            padx = kwargs.pop("padx", styles.PADDING_MEDIUM),
            pady = kwargs.pop("pady", styles.PADDING_MEDIUM),

            # Define os parâmetros restantes que foram recebidos.
            **kwargs
        )


    # Método que sobrescreve o método "grid()" da super classe para que já possua certas customizações pré-definidas.
    # ├─ self: referência ao próprio objeto.
    # ├─ row: posição da linha que irá ocupar no layout de tabela.
    # ├─ column: posição da coluna que irá ocupar no layout da tabela.
    # └─ **kwargs: qualquer valor recebido neste método, desde que não seja outro parâmetro, será armazenado nesta variável (opcional).
    def grid(self, row:int, column:int, **kwargs)->None:

        # Chama o método "grid()" da super classe para exibir o componente em um layout de tabela.
        super().grid(

            # Define a posição.
            row = row, # Número da linha na tabela.
            column = column, # Número da coluna na tabela.

            # Espaçamentos externos do componente
            padx = kwargs.pop("padx", styles.PADDING_MEDIUM),
            pady = kwargs.pop("pady", styles.PADDING_MEDIUM),

            # Define os parâmetros restantes que foram recebidos.
            **kwargs
        )

    def minimizar(self):
      
        if self.visible:
            self.model_frame.pack_forget()
            self.visible = False
        else:
            self.model_frame.pack(in_ = self)
            self.visible = True