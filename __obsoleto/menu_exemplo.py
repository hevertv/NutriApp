import tkinter as tk

from source.component.title_label import TitleLabel
from source.component.form_combobox import FormCombobox
from source.component.form_entry import FormEntry
from source.component.form_label import FormLabel
from source.component.form_text import FormText
from source.component.model_frame import ModelFrame
from source.component.model_button import ModelButton

class MenuExemplo(tk.Frame):

    # Atributo para armazenar o "pai" do menu.
    parent = None

    # Método construtor.
    # ├─ self: referência ao próprio objeto.
    # └─ parent: janela "pai" para a inserção do menu.
    def __init__(self, parent, open_menu)->None:

        self.parent = parent

        # Chama o construtor de "tk.Frame" para inicializar o container.
        super().__init__(
            parent, # Define a janela pai.
            bg = self.parent["bg"] # Cor de fundo.
        )
        self.pack() # Insere o menu na janela pai.

        title = TitleLabel(
            self,
            text = "Exemplo de campos."
        )
        title.pack()

        frame_form = ModelFrame(self)
        frame_form.pack()

        # - - - - - - - -

        # Entry 2 colunas.
        label2colunas = FormLabel(
            frame_form,
            text = "Exemplo de entry em 2 colunas."
        )
        label2colunas.grid(
            row = 0,
            column = 0
        )
        entry2colunas = FormEntry(
            frame_form
        )
        entry2colunas.grid(
            row = 1,
            column = 0,
            columnspan = 2
        )

        # - - - - - - - -

        # Entry comum.
        labelcomum = FormLabel(
            frame_form,
            text = "Exemplo de entry comum"
        )
        labelcomum.grid(
            row = 2,
            column = 0
        )
        entry_comum = FormEntry(
            frame_form
        )
        entry_comum.grid(
            row = 3,
            column = 0
        )
        
        # - - - - - - - -

        # Combobox (dropdown).
        label_combobox = FormLabel(
            frame_form,
            text = "Exemplo de combobox"
        )
        label_combobox.grid(
            row = 2,
            column = 1
        )
        combobox = FormCombobox(
            frame_form,
            values = ["Opção 1", "Opção 2", "Opção 3"]
        )
        combobox.grid(
            row = 3,
            column = 1
        )
        
        # - - - - - - - -

        # Text (textarea).
        label_text = FormLabel(
            frame_form,
            text = "Exemplo de text area em 2 colunas."
        )
        label_text.grid(
            row = 4,
            column = 0
        )
        text = FormText(
            frame_form
        )
        text.grid(
            row = 5,
            column = 0,
            columnspan = 2
        )
        
        # - - - - - - - -

        # Botões lado a lado
        button_voltar = ModelButton(
            frame_form,
            text = "Voltar",
            bootstyle = "primary-link" # Deixa sem cor de fundo.
        )
        button_voltar.grid(
            row = 6,
            column = 0,
            sticky = "w" # Gruda na esquerda do layout.
        )

        button_salvar = ModelButton(
            frame_form,
            text = "Salvar"
        )
        button_salvar.grid(
            row = 6,
            column = 1,
            sticky = "e" # Gruda na direita do layout.
        )

        # - - - - - - -
        