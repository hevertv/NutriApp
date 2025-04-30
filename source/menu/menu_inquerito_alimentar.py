"""
Menu para o formulário de "InqueritoAlimentar".
"""

import ttkbootstrap as ttk
from datetime import datetime

from source.toast import Toast
from source.pattern import Pattern
from source.banco_dados import BancoDados
from source.component.title_label import TitleLabel
from source.component.model_frame import ModelFrame
from source.component.form_label import FormLabel
from source.component.form_entry import FormEntry
from source.component.form_text import FormText
from source.component.form_combobox import FormCombobox
from source.component.model_button import ModelButton
from source.component.scrollable_frame import ScrollableFrame
from source.component.background_image_label import BackgroundImageLabel

PATH_BACKGROUND:str = "source/image/background.png" # Armazena o caminho para a imagem de fundo.

class MenuInqueritoAlimentar(ttk.Frame):

    parent = None # Janela pai.
    open_menu = None
    banco_dados = None

    # Atributos dos entries para ser possível obter seus valores no futuro.
    # inserir aqui os inputs.

    # Método construtor.
    # └─ parent: janela pai.
    def __init__(self, parent, open_menu, banco_dados:BancoDados)->None:

        self.parent = parent
        self.open_menu = open_menu
        self.banco_dados = banco_dados

        super().__init__(
            parent, # Janela pai.
        )
        self.pack()

        # Adiciona um frame com scroll na página.
        frame_scroll = ScrollableFrame(self)
        frame_scroll.pack()

        # Cria a imagem de fundo.
        menu_background = BackgroundImageLabel(frame_scroll, PATH_BACKGROUND)
        menu_background.place()

        # Título da página.
        title = TitleLabel(frame_scroll, text = "Inquérito Alimentar")
        title.pack()

        # Container para o formulário.
        frame_form = ModelFrame(frame_scroll)
        frame_form.pack()

        # Campos do formulário.
        label_desjejum = FormLabel(frame_form, text="Desjejum")
        label_desjejum.grid(row=0, column=0)
        self.input_desjejum = FormText(frame_form)
        self.input_desjejum.grid(row=1, column=0)
        label_desjejum_horario = FormLabel(frame_form, text="Horário")
        label_desjejum_horario.grid(row=0, column=1)
        self.input_desjejum_horario = FormEntry(frame_form, pattern = Pattern.CLOCK, pattern_block_input = True)
        self.input_desjejum_horario["width"] = int(self.input_desjejum_horario["width"] / 3)
        self.input_desjejum_horario.grid(row=1, column=1)
        
        label_lanche_manha = FormLabel(frame_form, text="Lanche da Manhã")
        label_lanche_manha.grid(row=2, column=0)
        self.input_lanche_manha = FormText(frame_form)
        self.input_lanche_manha.grid(row=3, column=0)
        label_lanche_manha_horario = FormLabel(frame_form, text="Horário")
        label_lanche_manha_horario.grid(row=2, column=1)
        self.input_lanche_manha_horario = FormEntry(frame_form)
        self.input_lanche_manha_horario["width"] = int(self.input_lanche_manha_horario["width"] / 3)
        self.input_lanche_manha_horario.grid(row=3, column=1)
        
        label_almoco = FormLabel(frame_form, text="Almoço")
        label_almoco.grid(row=4, column=0)
        self.input_almoco = FormText(frame_form)
        self.input_almoco.grid(row=5, column=0)
        label_almoco_horario = FormLabel(frame_form, text="Horário")
        label_almoco_horario.grid(row=4, column=1)
        self.input_almoco_horario = FormEntry(frame_form)
        self.input_almoco_horario["width"] = int(self.input_almoco_horario["width"] / 3)
        self.input_almoco_horario.grid(row=5, column=1)
        
        label_lanche_tarde = FormLabel(frame_form, text="Lanche da Tarde")
        label_lanche_tarde.grid(row=6, column=0)
        self.input_lanche_tarde = FormText(frame_form)
        self.input_lanche_tarde.grid(row=7, column=0)
        label_lanche_tarde_horario = FormLabel(frame_form, text="Horário")
        label_lanche_tarde_horario.grid(row=6, column=1)
        self.input_lanche_tarde_horario = FormEntry(frame_form)
        self.input_lanche_tarde_horario["width"] = int(self.input_lanche_tarde_horario["width"] / 3)
        self.input_lanche_tarde_horario.grid(row=7, column=1)
        
        label_jantar = FormLabel(frame_form, text="Jantar")
        label_jantar.grid(row=8, column=0)
        self.input_jantar = FormText(frame_form)
        self.input_jantar.grid(row=9, column=0)
        label_jantar_horario = FormLabel(frame_form, text="Horário")
        label_jantar_horario.grid(row=8, column=1)
        self.input_jantar_horario = FormEntry(frame_form)
        self.input_jantar_horario["width"] = int(self.input_jantar_horario["width"] / 3)
        self.input_jantar_horario.grid(row=9, column=1)
        
        label_ceia = FormLabel(frame_form, text="Ceia")
        label_ceia.grid(row=10, column=0)
        self.input_ceia = FormText(frame_form)
        self.input_ceia.grid(row=11, column=0)
        label_ceia_horario = FormLabel(frame_form, text="Horário")
        label_ceia_horario.grid(row=10, column=1)
        self.input_ceia_horario = FormEntry(frame_form)
        self.input_ceia_horario["width"] = int(self.input_ceia_horario["width"] / 3)
        self.input_ceia_horario.grid(row=11, column=1)
        
        label_outras = FormLabel(frame_form, text="Outras")
        label_outras.grid(row=12, column=0)
        self.input_outras = FormText(frame_form)
        self.input_outras.grid(row=13, column=0)
        label_outras_horario = FormLabel(frame_form, text="Horário")
        label_outras_horario.grid(row=12, column=1)
        self.input_outras_horario = FormEntry(frame_form)
        self.input_outras_horario["width"] = int(self.input_outras_horario["width"] / 3)
        self.input_outras_horario.grid(row=13, column=1)
        
        button_voltar = ModelButton(frame_form, text = "Voltar", bootstyle = "primary-link", command = lambda: open_menu("perfil_nutricional"))
        button_voltar.grid(row = 14, column = 0, sticky = "w")
        button_salvar = ModelButton(frame_form, text = "Salvar", command = self.salvar)
        button_salvar.grid(row = 14, column = 1, sticky = "e")

        # Foca este input quando o menu for exibido ao usuário.
        self.input_desjejum.focus()
        
    
    def salvar(self)->None:

        inserido = self.banco_dados.create(
            "inquerito_alimentar",
            {
                "id_paciente": self.banco_dados.id_paciente,
                "desjejum": self.input_desjejum.get(),
                "desjejum_horario": self.input_desjejum_horario.get(),
                "lanche_manha": self.input_lanche_manha.get(),
                "lanche_manha_horario": self.input_lanche_manha_horario.get(),
                "almoco": self.input_almoco.get(),
                "almoco_horario": self.input_almoco_horario.get(),
                "lanche_tarde": self.input_lanche_tarde.get(),
                "lanche_tarde_horario": self.input_lanche_tarde_horario.get(),
                "jantar": self.input_jantar.get(),
                "jantar_horario": self.input_jantar_horario.get(),
                "ceia": self.input_ceia.get(),
                "ceia_horario": self.input_ceia_horario.get(),
                "outras": self.input_outras.get(),
                "outras_horario": self.input_outras_horario.get(),
                "data_criacao": datetime.now().date().strftime("%d/%m/%Y")
            }
        )

        if inserido:

            # Altera de tela.
            Toast.success("Inquérito Alimentar cadastrado ao paciente.")
            self.open_menu("perfil_nutricional")
        
        else:
            Toast.danger("Ocorreu um erro no cadastro do inquérito alimentar.")