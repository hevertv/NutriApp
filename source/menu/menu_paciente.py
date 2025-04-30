import ttkbootstrap as ttk
from tkinter import filedialog
from datetime import datetime

import source.styles as styles
from source.banco_dados import BancoDados
from source.toast import Toast
from source.component.form_label import FormLabel
from source.component.form_entry import FormEntry
from source.component.model_frame import ModelFrame
from source.component.model_button import ModelButton
from source.component.form_combobox import FormCombobox
from source.component.title_label import TitleLabel
from source.pattern import Pattern
from source.component.background_image_label import BackgroundImageLabel

PATH_BACKGROUND = "source/image/background.png" # Armazena o caminho para a imagem de fundo.


class MenuPaciente(ttk.Frame):

    parent = None

    entry_nome = None
    entry_email = None
    entry_telefone = None
    entry_estado_civil=None
    entry_data_nascimento=None
    entry_sexo=None

     #vamos criar o metodo de contrucao 

    def __init__(self, parent, open_menu, banco_dados:BancoDados):
        
        self.parent = parent
        self.open_menu = open_menu
        self.banco_dados = banco_dados

     # definicao com a mesma cor da janela pai
        super().__init__(
            parent
        )

     #criacao do label "cadastro do paciente".
        self.pack()

        # Cria a imagem de fundo.
        menu_background = BackgroundImageLabel(self, PATH_BACKGROUND)
        menu_background.place()

        label_title = TitleLabel(
            self,
            text = "Cadastro de Paciente"
        )
        #criacao do label "cadastro do paciente".
        label_title.pack()

        frame_form = ModelFrame(
            self
        )
        frame_form.pack()

        label_nome = FormLabel(
            frame_form,
            text = "Nome Completo*"
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
            column = 0,
            columnspan=2,
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
            column = 0
        )

        label_telefone = FormLabel(
            frame_form,
            text = "Telefone*"
        )

        label_telefone.grid(
            row = 2,
            column = 1
        )

        self.entry_telefone = FormEntry(
            frame_form,
            pattern = Pattern.PHONE,
            pattern_block_input = True
        )
        self.entry_telefone.grid(
            row = 3,
            column = 1
        )

        ################# CRIANDO O LABEL SEXO##################################################################
        label_sexo=FormLabel(
            frame_form,
            text="Sexo*"

        )
        label_sexo.grid(
            row=4,
            column=0
        )
        
        
        self.entry_sexo=FormCombobox(
            frame_form,
            values = ["Masculino", "Feminino"]
        )
        self.entry_sexo.grid(
            row=5,
            column=0
        )
        #@@@@@@@@@@@@@@ FIM DO LABEL SEXO @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

        label_estado_civil = FormLabel(
            frame_form,
            text = "Estado Civil*"
        )
        label_estado_civil.grid(
            row = 4,
            column = 1
        )

        self.entry_estado_civil = FormCombobox(
            frame_form,
            values = ["Solteiro(a)", "Casado(a)", "Divorciado(a)", "Viúvo(a)"]
        )
        self.entry_estado_civil.grid(
            row = 5,
            column = 1
        )

        #DATA DE NASCIMENTO ############################################################################

        label_data_nacimento=FormLabel(
            frame_form,
            text="Data de Nascimento*"
        )
        label_data_nacimento.grid(
            row=6,
            column=0
        )

        self.entry_data_nascimento = ttk.DateEntry(
            frame_form
        )
        self.entry_data_nascimento.grid(row = 7, column = 0, sticky = "nswe", padx = styles.PADDING_SMALL, pady = (styles.PADDING_SMALL, styles.PADDING_LARGE))


        #FIM DO DATA DE NASCIMENTO@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

        label_naturalidade = FormLabel(frame_form, text = "Naturalidade*")
        label_naturalidade.grid(row = 6, column = 1)
        self.entry_naturalidade = FormEntry(frame_form, pattern = Pattern.NAME, pattern_block_input = True, warning_message = "Insira uma naturalidade válida.")
        self.entry_naturalidade.grid(row = 7, column = 1)

        label_raca = FormLabel(frame_form, text = "Raça*")
        label_raca.grid(row = 9, column = 0)
        self.entry_raca=FormCombobox(frame_form, values = ["Branco", "Pardo", "Preto", "Amarelo", "Indígena"])
        self.entry_raca.grid(row=10, column=0)

        label_foto = FormLabel(frame_form, text = "Foto do paciente")
        label_foto.grid(row = 9, column = 1)

        frame_foto = ttk.Frame(frame_form)
        frame_foto.grid(row = 10, column = 1)
        
        self.entry_foto = FormEntry(frame_foto, width = 11)
        self.entry_foto.grid(row = 0, column = 0)
        button_foto = ModelButton(frame_foto, text = "Escolher", bootstyle = "outline", command = self.__carregar_imagem)
        button_foto.grid(row = 0, column = 1, sticky = "nw", padx = 0, pady = styles.PADDING_SMALL)

        button_voltar = ModelButton(
            frame_form,
            text = "Voltar",
            bootstyle = "primary-link", # Deixa sem cor de fundo.
            command=lambda:self.open_menu("paciente_lista")
        )
        button_voltar.grid(
            row = 11,
            column = 0,
            sticky = "w" # Gruda na esquerda do layout.
        )

        button_salvar = ModelButton(
            frame_form,
            text = "Salvar",
            command = self.salvar
        )
        button_salvar.grid(
            row = 11,
            column = 1,
            sticky = "e" # Gruda na direita do layout.
        )

        # Foca o input quando o usuário visualizar pela primeira vez.
        self.entry_nome.focus()
        


    # Método para carregar a imagem do paciente.
    def __carregar_imagem(self)->None:
        filename = filedialog.askopenfilename(initialdir="/", title = "Selecione a foto do paciente.", filetypes=(("Arquivos PNG", "*.png"),))
        self.entry_foto.delete(0, "end")
        self.entry_foto.insert(0, filename)


    def salvar(self)->None:
        
        def ler_imagem(caminho_imagem)->None:
            if not caminho_imagem:
                return ""
            with open(caminho_imagem, 'rb') as arquivo_imagem:
                dados = arquivo_imagem.read()
            return dados.hex()
        dados_imagem = ler_imagem(self.entry_foto.get())
        
        inserido = self.banco_dados.create(
            "paciente",
            {
                "id_nutricionista": self.banco_dados.id_nutricionista,
                "nome": self.entry_nome.get(),
                "email": self.entry_email.get(),
                "telefone": self.entry_telefone.get(),
                "estado_civil": self.entry_estado_civil.get(),
                "data_nascimento": self.entry_data_nascimento.entry.get(),
                "sexo": self.entry_sexo.get(),
                "raca": self.entry_raca.get(),
                "naturalidade": self.entry_naturalidade.get(),
                "foto": dados_imagem,
                "data_criacao": datetime.now().date().strftime("%d/%m/%Y")
            }
        )

        if inserido:
            Toast.success("Paciente cadastrado com sucesso.")
            self.open_menu("paciente_lista")
        else:
            Toast.danger("Ocorreu um erro no cadastro do paciente!")