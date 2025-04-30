"""
Classe com todos os "patterns" que podem ser utilizados para a validação de dados
inseridos em Entries.
"""

from enum import Enum # Utilizada para enumerar um conjunto de constantes.

class Pattern(Enum):

    # Constantes para os patterns.
    NONE = None # Sem verificação.
    FLOAT_POSITIVE = r"^[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?$" # Apenas números acima de 0.
    EMAIL = r"[\w\.-]+@[\w\.-]+\.[\w]+" # Apenas padrões de e-mail.
    NAME = r"^(?!.*  )(?! )[A-Za-zÀ-ÿ ]+$" # Permite apenas letras, acentos e espaços.
    PHONE = r"^[0-9]{1,11}$" # Permite apenas números de no máximo 11 dígitos.
    PASSWORD = r"^.{8,}$" # Permite ter no mínimo 8 caracteres.
    CLOCK = r"^(?:2[0-3]?|[01]?\d?)?(?::[0-5]?\d?)?$" # Apenas padrões de relógio (24:00).
