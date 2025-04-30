"""

Classe para manter as informações de controle de um campo de um formulário,
como texto de exibição, validações e outras coisas.

Como utilizar?
├─ 1. Importar a classe.
└─ 2. Inicializar o objeto.

Exemplo:
from source.component.form_control import FormControl
campo_altura = FormControl("Insia a sua altura")

"""


# Classe para o controle de um campo de um formulário.
class FormControl:

    # Valor para a validação de um input que só deve receber números positivos.
    PATTERN_FLOAT_POSITIVE = r"^[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?$"

    # Atributos para o controle do campo.
    text:str = "" # Texto para exibir no Label.
    pattern:str = "" # String para a validação do texto inserido.

    # Outras ideias de implementação futuras (se for necessário).
    # required:bool # Para campos obrigatórios.
    # value_min:float # Valor mínimo para um campo numérico.
    # value_max:float # Valor máximo para um campo numérico.
    # length_min:int # Comprimento mínimo do texto inserido.
    # length_max:int # Comprimento máximo do texto inserido.

    # Método construtor.
    # ├─ self: referência ao próprio objeto.
    # ├─ text: texto para exibir no Label.
    # └─ pattern: String para validação do texto inserido (opcional).
    def __init__(self, text:str, pattern:str = "")->None:

        # Define os valores do objeto.
        self.text = text
        self.pattern = pattern
