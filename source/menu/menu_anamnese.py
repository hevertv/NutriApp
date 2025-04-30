"""
Menu para o formulário de "Anamnese".
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


class MenuAnamnese(ttk.Frame):

    parent = None # Janela pai.
    open_menu = None
    banco_dados = None

    parente = None

    entry_profissao = None
    entry_etilismo = None
    entry_atividade_fisica = None
    entry_tabagismo = None
    entry_doencas = None
    entry_questoes_familiares = None
    entry_questoes_religiosas = None
    entry_tradicoes = None
    entry_questoes_sociais = None


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
        title = TitleLabel(frame_scroll, text = "Anamnese")
        title.pack()

        # Container para o formulário.
        frame_form = ModelFrame(frame_scroll)
        frame_form.pack()


        # Campos do formulário.
        label_profissao = FormLabel(frame_form, text="Profissão")
        label_profissao.grid(row=0, column=0)
        self.entry_profissao = FormEntry(
            frame_form, 
            pattern = Pattern.NAME,
            pattern_block_input = True, 
            warning_message = "Insira sua profissão."
        )
        self.entry_profissao.grid(row=1, column=0)

        

        label_questoes_familiares = FormLabel(frame_form, text="Historia Familiar")
        label_questoes_familiares.grid(row=10, column=1)
        self.entry_questoes_familiares = FormText(
            frame_form, 
        )
        self.entry_questoes_familiares.grid(row=11, column=1)


        label_atividade_fisica = FormLabel(frame_form, text="Atividade Física")
        label_atividade_fisica.grid(row=2, column=0)
        self.entry_atividade_fisica = FormCombobox(
            frame_form,
            values = ["Sim", "Não"]
        )  
        self.entry_atividade_fisica.grid(row=3, column=0)

        label_etilismo = FormLabel(frame_form, text="Etilismo")
        label_etilismo.grid(row=0, column=1)
        self.entry_etilismo = FormCombobox(
            frame_form,
            values = ["Sim", "Não"]
        )
        self.entry_etilismo.grid(row=1, column=1)


        label_tabagismo = FormLabel(frame_form, text="Tabagismo")
        label_tabagismo.grid(row=2, column=1)
        self.entry_tabagismo = FormCombobox(
            frame_form,
            values = ["Sim", "Não"]
        )
        self.entry_tabagismo.grid(row=3, column=1)
        

        label_doencas = FormLabel(frame_form, text="Doenças")
        label_doencas.grid(row=10, column=0)
        self.entry_doencas = FormEntry(
            frame_form,
            pattern = Pattern.NAME,
            pattern_block_input = True, 
            warning_message = "Doença pré-existente ou crônica."
        )
        self.entry_doencas.grid(row=11, column=0)


        label_questoes_religiosas = FormLabel(frame_form, text="Religião")
        label_questoes_religiosas.grid(row=12, column=0)
        self.entry_questoes_religiosas = FormEntry(
            frame_form,
            pattern = Pattern.NAME,
            pattern_block_input = True, 
            warning_message = "Escreva qual é a sua religião." 
        )
        self.entry_questoes_religiosas.grid(row=13, column=0)


        label_tradicoes = FormLabel(frame_form, text="Questões Religiosas")
        label_tradicoes.grid(row=12, column=1)
        self.entry_tradicoes = FormText(
            frame_form,
        )
        self.entry_tradicoes.grid(row=13, column=1)


        label_questoes_sociais = FormLabel(frame_form, text="Questões Sociais")
        label_questoes_sociais.grid(row=14, column=0)
        self.entry_questoes_sociais = FormText(
            frame_form,
        )
        self.entry_questoes_sociais.grid(row=15, column=0, columnspan= 2)
        

        button_voltar = ModelButton(frame_form, text = "Voltar", bootstyle = "primary-link", command = lambda: open_menu("perfil_nutricional"))
        button_voltar.grid(row = 16, column = 0, sticky = "w")
        button_salvar = ModelButton(frame_form, text = "Salvar", command = self.salvar)
        button_salvar.grid(row = 16, column = 1, sticky = "e")

        # Foca este input quando o menu for exibido ao usuário.
        self.entry_profissao.focus()
        
    
    def salvar(self)->None:

        inserido = self.banco_dados.create(
            "anamnese",
            {
                "id_paciente": self.banco_dados.id_paciente,
                "profissao": self.entry_profissao.get(),
                "etilismo": self.entry_etilismo.get(),
                "atividade_fisica": self.entry_atividade_fisica.get(),
                "tabagismo": self.entry_tabagismo.get(),
                "doencas": self.entry_doencas.get(),
                "questoes_familiares": self.entry_questoes_familiares.get(),
                "questoes_religiosas": self.entry_questoes_religiosas.get(),
                "questoes_sociais": self.entry_questoes_sociais.get(),
                "tradicoes": self.entry_tradicoes.get(),
                "data_criacao": datetime.now().date().strftime("%d/%m/%Y")
            }
        )

        if inserido:

            # Altera de tela.
            Toast.success("Anamnese cadastrada ao paciente.")
            self.open_menu("perfil_nutricional")
        
        else:
            Toast.danger("Ocorreu um erro no cadastro da anamnese.")