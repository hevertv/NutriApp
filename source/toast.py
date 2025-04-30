"""
Arquivo para criar notificações que são exibidas ao usuário.
Nota: para facilitar a integração, todos os atributos e métodos são armazenados na classe, ao invés do objeto.
"""


import ttkbootstrap as ttk
from typing import List

import source.styles as styles

# Constantes apenas para armazenar os caminhos dos ícones utilizados.
PATH_CLOSE = "source/image/close_light.png"
PATH_DANGER = "source/image/danger_light.png"
PATH_INFO = "source/image/info_light.png"
PATH_SUCCESS = "source/image/success_light.png"
PATH_WARNING = "source/image/warning_light.png"


class Toast():

    TOAST_MAX_WIDTH:int = 256 # Constante para a largura máxima das notificações.
    TOAST_LIFETIME:int = 5000 # Constante para o tempo máximo de vida de um Toast.

    main_window:ttk.Window = None # Janela do aplicativo para criar as notificações.
    icon_close:ttk.PhotoImage = None # Ícone exibido no botão de fechar o Toast.
    icon_warning:ttk.PhotoImage = None # Ícone exibido quando o Toast for de "warning" (amarelo).
    icon_danger:ttk.PhotoImage = None # Ícone exibido quando o Toast for de "danger" (vermelho).
    icon_info:ttk.PhotoImage = None # Ícone exibido quando o Toast for de "info" (azul).
    icon_success:ttk.PhotoImage = None # Ícone exibido quando o Toast for de "success" (verde).
    toasts:List[ttk.Frame] = [] # Lista com todos os toasts existentes.

    
    # Método estático para reposicionar os toasts quando houver alguma alteração na tela.
    @staticmethod
    def __replace_all_toasts()->None:
        
        # Obtém as dimensões da janela para posicionar os toasts existentes.
        x = Toast.main_window.winfo_width() - styles.PADDING_MEDIUM - Toast.TOAST_MAX_WIDTH
        y = Toast.main_window.winfo_height() - styles.PADDING_MEDIUM

        # Posiciona todos os toasts existentes.
        for frame_toast in Toast.toasts[::-1]: # Obtém os valores do array na ordem inversa.

            # Posiciona o Toast de acordo com suas dimensões.
            y -= (frame_toast.winfo_reqheight() + styles.PADDING_MEDIUM)
            frame_toast.place(x = x, y = y, width = Toast.TOAST_MAX_WIDTH)


    # Método estático para deletar um toast ao clicar nele ou automaticamente após alguns segundos.
    # └─ frame_toast: o toast para deletar.
    @staticmethod
    def __destroy_toast(frame_toast:ttk.Frame)->None:

        # Verifica se o toast já não foi deletado (para evitar erros).
        if frame_toast in Toast.toasts:

            # Deleta o toast.
            Toast.toasts.remove(frame_toast)
            frame_toast.destroy()

            # Reposiciona os toasts que restaram.
            Toast.__replace_all_toasts()


    # Método estático para criar um toast e exibir na tela.
    # ├─ bootstyle: o estilo do Toast (danger, success, primary, etc).
    # ├─ title: texto exibido no topo do Toast.
    # ├─ text: mensagem para exibir ao usuário dentro do Toast.
    # └─ icon_title: ícone exibido no topo do Toast de acordo com o tipo de notificação.
    # Nota: eu poderia criar um componente para isto, mas preferi deixar aqui, sem nenhuma razão específica.
    @staticmethod
    def __create_toast(bootstyle:str, title:str, text:str, icon:ttk.PhotoImage)->ttk.Frame:

        # Frame principal para o Toast.
        frame_toast = ttk.Frame(
            Toast.main_window,
            cursor = "hand2"
        )

        # Frame da parte superior do Toast.
        frame_top = ttk.Frame(
            frame_toast,
            bootstyle = bootstyle,
            cursor = "hand2",
            padding = styles.PADDING_SMALL
        )
        frame_top.pack(fill = "x")
        frame_top.columnconfigure((0, 1), weight = 1) # Força para ocupar todo o espaço disponível.

        # Label para o título, com o ícone à esquerda.
        label_title = ttk.Label(
            frame_top,
            anchor = "w",
            bootstyle = f"{bootstyle}-inverse",
            compound = "left",
            cursor = "hand2",
            font = (styles.FONT, styles.FONT_SIZE_MEDIUM, "bold"),
            image = icon,
            text = title
        )
        label_title.grid(row = 0, column = 0, sticky = "w") # Gruda na esquerda do layout.

        # Botão para de fechar.
        button_close = ttk.Button(
            frame_top,
            bootstyle = bootstyle,
            command = lambda: Toast.__destroy_toast(frame_toast),
            image = Toast.icon_close,
            takefocus = 0
        )
        button_close.grid(row = 0, column = 1, sticky = "e") # Gruda na direita do layout.

        # Label para exibir a mensagem da notificação.
        label_message = ttk.Label(
            frame_toast,
            anchor = "nw",
            bootstyle = "light-inverse",
            cursor = "hand2",
            font = (styles.FONT, styles.FONT_SIZE_MEDIUM),
            padding = styles.PADDING_SMALL,
            text = text,
            wraplength = Toast.TOAST_MAX_WIDTH
        )
        label_message.pack(fill = "both", expand = True)

        # Gambiarra para fazer com que seja possível deletar o Toast apenas clicando em qualquer widget dele (ao invés de ser necessário clicar no botão X).
        # Nota: por causa disto eu coloquei "cursor = 'hand2'" nos widgets acima.
        frame_top.bind("<Button-1>", lambda _: Toast.__destroy_toast(frame_toast))
        label_title.bind("<Button-1>", lambda _: Toast.__destroy_toast(frame_toast))
        label_message.bind("<Button-1>", lambda _: Toast.__destroy_toast(frame_toast))

        # Insere o toast na estrutura.
        Toast.toasts.append(frame_toast)
        Toast.__replace_all_toasts()

        # Caso o usuário não interaja com o Toast, ele é deletado automaticamente.
        frame_toast.after(Toast.TOAST_LIFETIME, lambda: Toast.__destroy_toast(frame_toast))


    # Método estático para definir as configurações iniciais na Main.
    # └─ main_window: recebe a janela principal do aplicativo para criar os Toasts nela.
    def setup(main_window:ttk.Window)->None:
        Toast.main_window = main_window
        Toast.main_window.bind("<Configure>", lambda _: Toast.__replace_all_toasts()) # Reposiciona os Toasts existentes quando o tamanho da tela for redimensionado.

        # Carrega as imagens os toasts.
        Toast.icon_warning = ttk.PhotoImage(file = PATH_WARNING).subsample(4)
        Toast.icon_close = ttk.PhotoImage(file = PATH_CLOSE).subsample(4)
        Toast.icon_danger = ttk.PhotoImage(file = PATH_DANGER).subsample(4)
        Toast.icon_info = ttk.PhotoImage(file = PATH_INFO).subsample(4)
        Toast.icon_success = ttk.PhotoImage(file = PATH_SUCCESS).subsample(4)
    

    # Método estático para criar um Toast de "danger" (vermelho).
    # └─ text: mensagem para exibir ao usuário dentro do Toast.
    @staticmethod
    def danger(text:str)->None:
        Toast.__create_toast("danger", "Erro!", text, Toast.icon_danger)


    # Método estático para criar um Toast de "info" (azul).
    # └─ text: mensagem para exibir ao usuário dentro do Toast.
    @staticmethod
    def info(text:str)->None:
        Toast.__create_toast("info", "Informativo", text, Toast.icon_info)


    # Método estático para criar um Toast de "success" (verde).
    # └─ text: mensagem para exibir ao usuário dentro do Toast.
    @staticmethod
    def success(text:str)->None:
        Toast.__create_toast("success", "Sucesso!", text, Toast.icon_success)


    # Método estático para criar um Toast de "warning" (amarelo).
    # └─ text: mensagem para exibir ao usuário dentro do Toast.
    @staticmethod
    def warning(text:str)->None:
        Toast.__create_toast("warning", "Alerta!", text, Toast.icon_warning)

