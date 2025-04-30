"""
Componente de Entry para formulários já possuindo as seguintes customizações:
    - Configurações de fonte.
    - Espaçamento externo.
    - Possibilidade de exibir uma mensagem de alerta na validação do input.
    - Possibilidade de definir o input para senha.
"""

import ttkbootstrap as ttk
import re # Utilizado na validação do input.

import source.styles as styles
from source.pattern import Pattern


class FormEntry(ttk.Entry):

    parent = None # Janela pai.
    label_warning:ttk.Label = None # Label para a mensagem de alerta.
    pattern:Pattern = Pattern.NONE # String de validação do valor inserido.
    warning_message:str = "" # Mensagem de alerta para o usuário quando o input não for validado.
    pattern_block_input:bool = False # Quando verdadeiro, inputs fora do pattern serão bloqueados.
    placeholder:str = "" # Mensagem exibida enquanto o usuário não selecionar o entry.

    # Método construtor.
    # ├─ parent: janela pai.
    # ├─ pattern (opcional): string de validação do valor inserido.
    # ├─ warning_message (opcional): mensagem de alerta para o usuário quando o input não for validado.
    # ├─ pattern_block_input (opcional): quando verdadeiro, inputs fora do pattern serão bloqueados.
    # ├─ placeholder (opcional): mensagem exibida quando o usuário não selecionar o entry.
    # ├─ is_password (opcional): quando verdadeiro, o Entry só irá exibir *.
    # ├─ width (opcional): largura do componente.
    # └─ **kwargs: parâmetros extras.
    def __init__(self, parent, pattern:Pattern = Pattern.NONE, warning_message:str = "", pattern_block_input:bool = False, placeholder:str = "", is_password:bool = False, width:int = 20, **kwargs)->None:

        self.parent = parent
        self.pattern = pattern
        self.warning_message = warning_message
        self.pattern_block_input = pattern_block_input
        self.placeholder = placeholder

        # Constrói o Entry.
        # └─ Nota: a janela pai só é definida no método "pack()", "grid()" ou "place()".
        super().__init__(
            width = width, # Largura do componente.
            font = kwargs.pop("font", (styles.FONT, styles.FONT_SIZE_MEDIUM)), # Configurações de fonte.
            **kwargs # Parâmetros extras.
        )

        # Label para exibir a mensagem de alerta.
        # └─ Nota: a janela pai só é definida no método "pack()", "grid()" ou "place()".
        self.label_warning = ttk.Label(
            anchor = "w", # Alinhamento do texto.
            bootstyle = "danger",
            font = (styles.FONT, styles.FONT_SIZE_MEDIUM)
        )
        
        # Quando existir um pattern, a validação é criada.
        if self.pattern != Pattern.NONE:

            # Define quando a validação deve ocorrer.
            if pattern_block_input:
                self["validate"] = "key" # A cada tecla pressionada.
            else:
                self["validate"] = "focusout" # Após perder o foco.
            
            # Armazena o método de validação.
            validate_command = (
                self.register(
                    lambda text:
                    self.__validate_value(text)
                ),
                "%P" # Obtém todo o texto digitado no Entry.
            )

            # Define o comando de validação
            self["validatecommand"] = validate_command

            # Quando o pattern bloqueia o input, também é feito uma verificação após o Entry perder foco.
            if pattern_block_input:
                super().bind("<FocusOut>", lambda _, text = self.get(): self.__validate_value(text))

        # Quando o Entry for para senha.
        if is_password:
            self["show"] = "*"
        
        # Caso o entry possua placeholder.
        if placeholder:
            super().bind("<FocusIn>", self.__focus_in)
            super().bind("<FocusOut>", self.__focus_out)
            self.__focus_out()


    # Método de validação do texto digitado.
    # └─ text: todo o texto digitado no componente.
    def __validate_value(self, text:str)->bool:

        # Quando o texto for vazio, sempre será lálido (sem isto não seria possível apagar todo o texto).
        if not text:
            self.label_warning["text"] = ""
            self.configure(bootstyle = "default")
            return True

        # Verifica se o texto é válido.
        valid = bool(re.match(self.pattern.value, text))

        # Esconde ou exibe o alerta de acordo com a validação.
        if valid:
            self.label_warning["text"] = ""
            self.configure(bootstyle = "default")
        else:
            self.label_warning["text"] = self.warning_message
            self.configure(bootstyle = "danger")
        
        # Quando o pattern não pode bloquear o input, deve retornar verdadeiro para não apagar o que foi digitado.
        if not self.pattern_block_input:
            valid = True
        
        # Quando pode bloquear, é tocado um som.
        elif valid == False:
            self.bell()
        
        return valid


    # Método para remover o placeholder, caso exista.
    def __focus_in(self, *args)->None:
        if super().get() == self.placeholder:
            self.delete(0, "end")
    

    # Método para aplicar o placeholder, caso exista.
    def __focus_out(self, *args)->None:
        if not super().get():
            self.insert(0, self.placeholder)


    # Sobrescreve o método "bind()" da super classe.
    def bind(self, key:str, method)->None:
        
        match key:
            case "<FocusIn>":
                super().bind("<FocusIn>", lambda _: (
                    method(),
                    self.__focus_in() if self.placeholder else None 
                ))
            case "<FocusOut>":
                super().bind("<FocusOut>", lambda _, text = self.get(): (
                    method(),
                    self.__focus_out() if self.placeholder else None,
                    self.__validate_value(text) if self.pattern and self.pattern_block_input else None
                ))
            case _:
                super().bind(key, method)


    # Sobrescreve o método "pack()" da super classe.
    # └─ **kwargs: parâmetros extras.
    def pack(self, **kwargs)->None:

        # Obtém os valores para alterar tanto no Entry quanto no Label de alerta.
        self.parent = kwargs.pop("in_", self.parent)
        fill = kwargs.pop("fill", "x")
        padx = kwargs.pop("padx", styles.PADDING_SMALL)

        super().pack(
            in_ = self.parent, # Janela pai.
            fill = fill, # Preenchimento.
            padx = padx, # Espaçamento externo x.
            pady = kwargs.pop("pady", 0), # Espaçamento externo y.
            **kwargs # Parâmetros extras.
        )

        # Insere o Label de alerta.
        self.label_warning.pack(
            in_ = self.parent, # Janela pai.
            fill = fill,# Preenchimento.
            padx = padx, # Espaçamento externo x.
            pady = 0 # Espaçamento externo y.
        )
    

    # Sobrescreve o método "grid()" da super classe.
    # ├─ row: número da linha.
    # ├─ column: número da coluna.
    # └─ **kwargs: parâmetros extras.
    def grid(self, row:int, column:int, **kwargs)->None:

        self.parent = kwargs.pop("_in", self.parent)
        
        # Cria um Frame para inserir o Entry e o Label de alerta.
        frame = ttk.Frame(
            self.parent, # Janela pai.
            padding = 0 # Espaçamento interno.
        )
        frame.grid(
            row = row, # Número da linha.
            column = column, # Número da coluna.
            sticky = kwargs.pop("sticky", "nsew"), # Preenchimento completo na célula.
            rowspan = kwargs.pop("rowspan", 1), # Quantidade de linhas que ocupa na tabela.
            columnspan = kwargs.pop("columnspan", 1), # Quantidade de colunas que ocupa na tabela.
            padx = kwargs.pop("padx", styles.PADDING_SMALL), # Espaçamento externo x.
            pady = kwargs.pop("pady", (styles.PADDING_SMALL, 0)) # Espaçamento externo y.
        )

        # Insere o Entry e o Label de alerta no Frame.
        super().pack(
            in_ = frame, # Janela pai.
            fill = "x", # Preenchimento.
            padx = 0, # Espaçamento externo x.
            pady = 0 # Espaçamento externo y.
        )

        self.label_warning.pack(
            in_ = frame, # Janela pai.
            fill = "x",# Preenchimento.
            padx = 0, # Espaçamento externo x.
            pady = 0 # Espaçamento externo y.
        )
    

    # Sobrescreve o método "get()" da super classe.
    def get(self)->str:

        input_text = super().get()
        if input_text == self.placeholder:
            input_text = ""
        
        return input_text
