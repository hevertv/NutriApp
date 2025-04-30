"""

Este arquivo é só um exemplo para testar a mudança de página no
aplicativo e que deve ser alterado posteriormente.

Como utilizar?
├─ 1. Importar a classe.
└─ 2. Inicializar o objeto.

Exemplo:
from source.menu.menu_exemplo import MenuExemplo
menu_exemplo = MenuExemplo(parent)

Nota: "Parent" é o espaço que o menu será exibido na janela do aplicativo.

"""


# Importações de bibliotecas.
import tkinter as tk # Biblioteca Tkinter.
import tkinter.font as tk_font # Biblioteca interna do Tkinter para customização de fontes.

# Importações do projeto.
import source.styles as styles # Arquivo de estilização.
from source.component.title_label import TitleLabel # Componente para o título.
from source.component.background_image_label import BackgroundImageLabel

from source.banco_dados import BancoDados


PATH_BACKGROUND = "source/image/configuracoes_background.png"


# Classe para a criação do menu.
# └─ (Frame): "MenuAgenda" também possui todos os atributos e métodos da classe "Frame".
class MenuConfiguracoes(tk.Frame):

    # Atributo para armazenar o "pai" do menu.
    parent = None

    # Método construtor.
    # ├─ self: referência ao próprio objeto.
    # └─ parent: janela "pai" para a inserção do menu.
    def __init__(self, parent, open_menu, banco_dados:BancoDados)->None:

        # Define que a variável seja o mesmo que o parâmetro recebido.
        self.parent = parent

        # Chama o construtor de "tk.Frame" para inicializar o container.
        super().__init__(
            parent, # Define a janela "pai" deste Frame.
        )

         # Cria a imagem de fundo.
        menu_background = BackgroundImageLabel(self, PATH_BACKGROUND)
        menu_background.place()

        # # Insere o container para ser exibido em sua janela "pai", de forma centralizada.
        # self.pack(fill = "both", expand = True)

        # Inicializa o título da página.
        title = TitleLabel(
            self, # Define a janela "pai" deste título.
            text = "Configurações" # Texto exibido no título
        )
        title.pack()

        # # Insere um Label para exibir um texto explicando o que é este menu.
        # label_info = tk.Label(
        #     self, # Define a janela "pai" deste título.
        #     text = "Aqui o usuário poderá configurar o aplicativo de acordo com a sua necessidade.",
        #     wraplength = 300, # Define para o texto pular para a próxima linha quando ultrapassar este tamanho.

        #     # Configurações extras da fonte do texto.
        #     font = tk_font.Font(
        #         family = styles.FONT, # Fonte utilizada.
        #         size = styles.FONT_SIZE_MEDIUM, # Tamanho do texto.
        #     )
        # )

        # # Insere o Label para ser exibido em sua janela "pai", de forma centralizada.
        # label_info.pack()