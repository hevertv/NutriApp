"""

Arquivo para a criação de um formulário com a formatação já definida, sendo
possível reutilizá-lo ao longo do projeto.

Como utilizar?
├─ 1. Importar a classe.
├─ 2. Definir os campos do formulário (utilizando a classe FormControl).
└─ 3. Inicializar o objeto.

Exemplo:
from source.component.form import Form
from source.component.form_control import FormControl
fields = {
    "altura": FormControl("Altura"),
    "peso": FormControl("Peso")
}
form = Form(parent, fields)

Nota: "parent" é o espaço que o formulário será exibido na janela do aplicativo.

"""


# Importações de bibliotecas.
import tkinter as tk # Biblioteca Tkinter.
import re # Biblioteca para validar uma String com base em um padrão escolhido.
from tkinter.font import Font # Classe para a customização de fontes.
from typing import Dict # Classe para um dicionário com chaves e valores de tipos específicos.

# Importações do projeto.
import source.styles as styles # Arquivo de estilização.
from obsoleto.form_control import FormControl # Classe para a criação dos campos do formulário.


# Classe para a criação do formulário.
class Form:

    # Atributos para armazenar o formulário.
    form:tk.Frame = None # Container do formulário.
    entries:Dict[str, tk.Entry] = {} # Dicionário para os inputs de entrada do formulário.
    

    # Método construtor.
    # ├─ self: referência ao próprio objeto.
    # ├─ parent: janela "pai" para a inserção do formulário.
    # ├─ fields: campos para serem criados.
    # └─ color_background: cor de fundo do formulário (opicional).
    def __init__(self, parent, fields:Dict[str, FormControl], color_background:str = styles.COLOR_FOREGROUND)->None:

        # Inicializa um container para o formulário.
        self.form = tk.Frame(
            parent, # Define a janela "pai" deste container.
            bg = color_background, # Cor de fundo do formulário.
            padx = styles.PADDING_MEDIUM, # Define o espaçamento horizontal interno deste container.
            pady = styles.PADDING_MEDIUM # Define o espaçamento vertical interno deste container.
        )

        # Insere o formulário para ser exibido em sua janela "pai", de forma centralizada.
        self.form.pack(
            padx = styles.PADDING_SMALL, # Define o espaçamento horizontal externo deste container.
            pady = styles.PADDING_SMALL # Define o espaçamento vertical externo deste container.
        )

        # Loop para a criação de todos os campos do formulário.
        # ├─ row_count: contador para posicionar os campos.
        # └─ field: chave para criar os campos.
        for row_count, field in enumerate(fields):

            # Configurações para cada linha criada no formulário.
            self.form.grid_rowconfigure(
                row_count, # Posição da linha.
                pad = styles.PADDING_MEDIUM # Define o espaçamento geral entre as linhas.
            )

            # Inicializa o Label para o campo.
            label = tk.Label(
                self.form, # Define a janela "pai" deste Label.
                text = fields[field].text + ": ", # Texto exibido no Label.
                bg = color_background, # Cor de fundo do texto.
                fg = styles.COLOR_FONT_DARK, # Cor do texto.

                # Configurações extras da fonte do texto.
                font = Font(
                    family = styles.FONT, # Fonte utilizada.
                    size = styles.FONT_SIZE_MEDIUM # Tamanho do texto.
                )
            )

            # Insere o Label em uma formatação de tabela.
            label.grid(
                row = row_count, # Posição da linha.
                column = 0, # Posição da coluna.
                sticky = "e" # Alinhamento do texto ("e" => east).
            )

            # Inicializa o input de entrada para o campo.
            entry = tk.Entry(
                self.form # Define a janela "pai" deste Entry.
            )

            # Condição para quando o Entry possui alguma restrição de valores recebidos (definido em FormControl).
            if fields[field].pattern != "":

                # Define quando a validação deve ocorrer.
                # └─ "key": validado a cada tecla pressionada.
                entry["validate"] = "key"

                # Armazena o método de validação para o Entry.
                # └─ "lambda": termo em Python para criar um método anônimo (sem uma declaração).
                validate_command = (
                    entry.register(
                        lambda text, pattern = fields[field].pattern:
                            self.__validate_value(text, pattern)
                    ),
                    "%P" # "%P" obtém todo o texto digitado no Entry.
                )

                # Define o comando de validação.
                entry["validatecommand"] = validate_command
            
            # Insere o Entry em uma formação de tabela.
            entry.grid(
                row = row_count, # Posição da linha.
                column = 1 # Posição da coluna.
            )

            # Armazena o Entry neste atributo, para ser possível obter seu valor no futuro.
            self.entries[field] = entry


    # Método de validação para um Entry do formulário.
    # ├─ self: referência ao próprio objeto.
    # ├─ text: todo o texto digitado no Entry.
    # └─ pattern: String para a validação do texto recebido (definido em FormControl).
    def __validate_value(self, text:str, pattern:str)->bool:

        # Sem essa confirmação, não seria possível apagar todo o texto digitado no Entry.
        if text == "":
            return True

        # Retorna True se o texto é válido, caso contrário, não será inserido no Entry.
        return bool(re.match(pattern, text))


    # Método para obter os valores dos Entries.
    # └─ self: referência ao próprio objeto.
    def get_form_data(self)->Dict[str, str]:
        
        # Atributo para armazenar os valores dos Entries.
        form_data = {}

        # Loop para obter os valores.
        for field, entry in self.entries.items():
            form_data[field] = entry.get()
        
        # Retorna os dados obtidos.
        return form_data
    
    
    # Método para destruir o formulário, removendo o container da exibição na janela.
    # └─ self: referência ao próprio objeto.
    def destroy(self)->None:
        self.form.destroy()
