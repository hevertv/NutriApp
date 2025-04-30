"""
Arquivo raiz da aplicação.
"""

import ttkbootstrap as ttk

from source.app import App
from source.styles import Styles
from source.toast import Toast

class Main(ttk.Window):

    # Método construtor.
    def __init__(self):

        # Constrói a janela da aplicação.
        super().__init__(
            themename="litera", # Tema de estilização.
            title = "NutriApp" # Texto exibido no topo da janela.
        )
        self.geometry("1280x720") # Dimenções da janela.
        self.minsize(1076, 600) # Dimenção mínima da janela.


# Inicializa a interface gráfica.
# └─ __name__: variável do Python, neste caso é definida como "__main__".
if __name__ == "__main__":

    # Cria a janela do aplicativo.
    main = Main()

    # Inicializa a configuração dos alertas.
    Toast.setup(main)

    # Inicializa as estilizações para o projeto.
    Styles()

    # Inicializa o aplicativo.
    App(main)

    main.mainloop()
