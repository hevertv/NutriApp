"""
Menu de cadastro de usuário.
"""


import ttkbootstrap as ttk
import json
from datetime import datetime

import source.styles as styles
from source.banco_dados import BancoDados
from source.pattern import Pattern
from source.toast import Toast
from source.component.form_label import FormLabel
from source.component.form_entry import FormEntry
from source.component.model_frame import ModelFrame
from source.component.model_button import ModelButton
from source.component.background_image_label import BackgroundImageLabel

PATH_BACKGROUND = "source/image/login_background.png" # Armazena o caminho para a imagem de fundo.
PATH_USER_DATA = "data/user_data.json" # Caminho do arquivo que armazena o login/senha do usuário.


class MenuNutricionista(ttk.Frame):

    parent = None # Janela pai.
    open_menu = None # Atributo para o método de referência para alterar de menu.
    banco_dados:BancoDados = None # Conexão com o banco de dados.

    # Salva os widgets do menu.
    entry_nome:FormEntry = None
    entry_telefone:FormEntry = None
    entry_email:FormEntry = None
    entry_senha:FormEntry = None
    entry_senha_repetir:FormEntry = None
    frame_information:ttk.Frame = None
    background:BackgroundImageLabel = None

    # Método construtor.
    # ├─ parent: janela pai.
    # ├─ open_menu: método de referência para alterar de menu.
    # └─ banco_dados: conexão com o banco de dados.
    def __init__(self, parent, open_menu, banco_dados:BancoDados)->None:

        self.parent = parent
        self.open_menu = open_menu
        self.banco_dados = banco_dados

        # Constrói o menu.
        super().__init__(parent)
        self.pack(fill = "both", expand = True)

        # Imagem de fundo.
        self.background = BackgroundImageLabel(self, path_image = PATH_BACKGROUND)
        self.background.place()

        # Frame para inserir as informações.
        self.frame_information = ttk.Frame(self, padding = (styles.PADDING_LARGE, 0), width = 520)
        self.frame_information.pack(fill = "y", side = "right")
        self.frame_information.pack_propagate(0) # Desabilita o redimensionamento automático.

        # CRIE O FORMULÁRIO A PARTIR DAQUI.
        # 1. Definir o título
        title = ttk.Label(
            self.frame_information,
            text = "Criar sua conta NutriApp",
            font = (styles.FONT, styles.FONT_SIZE_INTERMEDIATE, "bold")
        )
        title.place(relx = 0.5, rely = 0.2, anchor = "center")


        frame_form = ModelFrame(
            self.frame_information
        )
        frame_form.place(relx = 0.5, rely = 0.5, anchor = "center")


        label_nome = FormLabel(
            frame_form,
            text = "Nome*"
        )
        label_nome.grid(
            row = 0,
            column = 0
        )

        self.entry_nome = FormEntry(
            frame_form,
            pattern = Pattern.NAME,
            pattern_block_input = True,
            warning_message = "Insira um nome válido."
        )
        self.entry_nome.grid(
            row = 1,
            column = 0
        )

        label_telefone = FormLabel(
            frame_form,
            text = "Telefone*"
        )

        label_telefone.grid(
            row = 0,
            column = 1
        )

        self.entry_telefone = FormEntry(
            frame_form,
            pattern = Pattern.PHONE,
            pattern_block_input = True
        )
        self.entry_telefone.grid(
            row = 1,
            column = 1
        )
    
        label_email = FormLabel(
            frame_form,
            text = "Email*"
        )

        label_email.grid(
            row = 2,
            column = 0
        )

        self.entry_email = FormEntry(
            frame_form,
            pattern = Pattern.EMAIL,
            warning_message = "Insira um e-mail válido."
        )
        self.entry_email.grid(
            row = 3,
            column = 0,
            columnspan = 2
        )

        label_senha = FormLabel(
            frame_form,
            text = "Senha*"
        )

        label_senha.grid(
            row = 4,
            column = 0
        )

        self.entry_senha = FormEntry(
            frame_form,
            is_password = True,
            pattern = Pattern.PASSWORD,
            warning_message = "Mínimo de 8 caracteres."
        )

        self.entry_senha.grid(
            row = 5,
            column = 0
        )

        label_senha_repetir = FormLabel(
            frame_form,
            text = "Repetir a senha*"
        )
        label_senha_repetir.grid(
            row = 4,
            column = 1
        )

        self.entry_senha_repetir = FormEntry(
            frame_form,
            is_password = True,
            pattern = Pattern.PASSWORD,
            warning_message = "Mínimo 8 caracteres."
        )
        self.entry_senha_repetir.grid(
            row = 5,
            column = 1
        )

        button_voltar = ModelButton(frame_form, text = "Voltar", bootstyle = "primary-link", command = lambda: self.open_menu("login"))
        button_voltar.grid(row = 6, column = 0, sticky = "w", padx = (styles.PADDING_SMALL, 0))

        button_enviar = ModelButton(frame_form, text = "Salvar", command = self.salvar)
        button_enviar.grid(row = 6, column = 1, sticky = "e", padx = (0, styles.PADDING_SMALL))

        # Isto corrige a ordem de seleção no formulário através da tecla TAB.
        button_voltar.lift()

        # Foca o input quando o usuário visualizar pela primeira vez.
        self.entry_nome.focus()


    def salvar(self):

        if self.entry_senha.get() != self.entry_senha_repetir.get():
            print(self.entry_senha.get() != self.entry_senha_repetir.get())
            Toast.danger("As senhas não são iguais. Tente novamente.")
            self.entry_senha_repetir.delete(0, "end")
            return

        inserido = self.banco_dados.create(
            "nutricionista",
            {
                "nome": self.entry_nome.get(),
                "telefone": self.entry_telefone.get(),
                "email": self.entry_email.get(),
                "senha": self.entry_senha.get(),
                "data_criacao": datetime.now().date().strftime("%d/%m/%Y")
            }
        )

        if inserido:
            try:
                with open(PATH_USER_DATA, "w") as file_opened:
                    data = {"email": self.entry_email.get(), "senha": self.entry_senha.get()}
                    json.dump(data, file_opened)
            except OSError as _:
                pass
            self.banco_dados.get_user_auth(email = self.entry_email.get(), senha = self.entry_senha.get())
        
            # Altera de tela.
            Toast.info("Seja bem vindo(a).")
            self.open_menu("paciente_lista")
        
        else:
            Toast.danger("Ocorreu um erro no cadastro!")
    
