import ttkbootstrap as ttk
from datetime import datetime

import source.styles as styles
from source.toast import Toast
from source.component.form_label import FormLabel
from source.component.form_entry import FormEntry
from source.component.model_frame import ModelFrame
from source.component.model_button import ModelButton
from source.component.title_label import TitleLabel
from source.pattern import Pattern
from source.component.background_image_label import BackgroundImageLabel

from source.banco_dados import BancoDados

PATH_BACKGROUND:str = "source/image/background.png" # Armazena o caminho para a imagem de fundo.


class MenuAntropometria(ttk.Frame):

    # Atributo para armazenar o "pai" do menu.
    parent = None
    open_menu = None
    banco_dados:BancoDados = None

    entry_peso = None
    entry_altura = None
    entry_circunferencia_cintura = None
    entry_composicao_corporal = None

    # Método construtor.
    # ├─ self: referência ao próprio objeto.
    # └─ parent: janela "pai" para a inserção do menu.
    def __init__(self, parent, open_menu, banco_dados:BancoDados)->None:

        self.parent = parent
        self.open_menu = open_menu
        self.banco_dados = banco_dados

        # Chama o construtor de "tk.Frame" para inicializar o container.
        super().__init__(
            parent, # Define a janela pai.
        )
        self.pack() # Insere o menu na janela pai.

        # Cria a imagem de fundo.
        menu_background = BackgroundImageLabel(self, PATH_BACKGROUND)
        menu_background.place()

        # CRIE O FORMULÁRIO A PARTIR DAQUI.
        # 1. Definir o título.
        title = TitleLabel(
            self,
            text = "Cadastrar Antropometria"
        )
        title.pack()
        

        frame_form = ModelFrame(
            self
        )
        frame_form.pack()
        
        
        label_peso = FormLabel(
            frame_form,
            text = "Peso*"
        )

        label_peso.grid(
            row = 0,
            column = 0,
        )
        

        self.entry_peso = FormEntry(
            frame_form,
            pattern = Pattern.FLOAT_POSITIVE,
            pattern_block_input = True
        )

        self.entry_peso.grid(
            row = 1,
            column = 0,
            columnspan = 2
        )
        
        label_altura = FormLabel(
            frame_form,
            text = "Altura (centimetros)*"
        )

        label_altura.grid(
            row = 2,
            column = 0
        )

        self.entry_altura = FormEntry(
            frame_form,
            pattern = Pattern.FLOAT_POSITIVE,
            pattern_block_input = True
        )

        self.entry_altura.grid(
            row = 3,
            column = 0,
            columnspan = 2
        )

        label_circunferencia_cintura = FormLabel(
            frame_form,
            text = "Circunferência da Cintura*"
        )

        label_circunferencia_cintura.grid(
            row = 4,
            column = 0
        )

        self.entry_circunferencia_cintura = FormEntry(
            frame_form,
            pattern = Pattern.FLOAT_POSITIVE,
            pattern_block_input = True
        )

        self.entry_circunferencia_cintura.grid(
            row = 5,
            column = 0,
            columnspan = 2
        )

        label_composicao_corporal = FormLabel(
            frame_form,
            text = "Composição Corporal*"
        )

        label_composicao_corporal.grid(
            row = 6,
            column = 0
        )

        self.entry_composicao_corporal = FormEntry(
            frame_form
        )

        self.entry_composicao_corporal.grid(
            row = 7,
            column = 0,
            columnspan = 2
        )


        button_voltar = ModelButton(frame_form, text = "Voltar", bootstyle = "primary-link", command = lambda: self.open_menu("perfil_nutricional"))
        button_voltar.grid(row = 8, column = 0, sticky = "w", padx = (styles.PADDING_SMALL, 0))

        button_enviar = ModelButton(frame_form, text = "Salvar", command = self.salvar)
        button_enviar.grid(row = 8, column = 1, sticky = "e", padx = (0, styles.PADDING_SMALL))

        # Foca este input quando o menu for exibido ao usuário.
        self.entry_peso.focus()


    def salvar(self):

        inserido = self.banco_dados.create(
            "antropometria",
            {
                "id_paciente": self.banco_dados.id_paciente,
                "peso": self.entry_peso.get(),
                "altura": self.entry_altura.get(),
                "circunferencia_cintura": self.entry_circunferencia_cintura.get(),
                "composicao_corporal": self.entry_composicao_corporal.get(),
                "data_criacao": datetime.now().date().strftime("%d/%m/%Y")
            }
        )

        if inserido:
            # Altera de tela.
            Toast.success("Antropometria cadastrada ao paciente.")
            self.open_menu("perfil_nutricional")
        else:
            Toast.danger("Ocorreu um erro no cadastro da antropometria.")
