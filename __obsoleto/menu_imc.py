"""

Arquivo contendo a classe que cria o menu para calcular o IMC digitado
pelo o usuário.

Como utilizar?
├─ 1. Importar a classe.
└─ 2. Inicializar o objeto.

Exemplo:
from source.menu.menu_imc import MenuImc
menu_imc = MenuImc(parent)

Nota: "parent" é o espaço que o menu será exibido na janela do aplicativo.

"""


# Importações de bibliotecas.
import tkinter as tk # Biblioteca Tkinter.
import tkinter.font as tk_font # Biblioteca interna do Tkinter para customização de fontes.

# Importações do projeto.
import source.styles as styles # Arquivo de estilização.
from source.component.model_button import ModelButton # Componente para a criação de botões.
from source.component.title_label import TitleLabel # Componente para o título.
from obsoleto.form import Form # Componente para a criação dos campos do formulário.
from obsoleto.form_control import FormControl # Componente para informações de controle dos campos do formulário.

# Campos para serem exibidos no formulário.
form_fields = {
    "altura": FormControl(
        text = "Altura (cm)",
        pattern = FormControl.PATTERN_FLOAT_POSITIVE
    ),
    "peso": FormControl(
        text = "Peso (kg)",
        pattern = FormControl.PATTERN_FLOAT_POSITIVE
    )
}

# Classe para a criação do menu para o cálculo do IMC.
# └─ (tk.Frame): "MenuImc" também possui todos os atributos e métodos da classe "Frame".
class MenuImc(tk.Frame):

    # Atributo para armazenar o "pai" do menu.
    parent = None

    # Variaveis para armazenar os valores do formulário.
    form = None # Armazena todo o formulário.
    label_result = None # Armazena o Label que exibe o resultado.

    # Método construtor.
    # ├─ self: referência ao próprio objeto.
    # └─ parent: janela "pai" para a inserção do menu.
    def __init__(self, parent)->None:

        # Define que a variável seja o mesmo que o parâmetro recebido.
        self.parent = parent

        # Chama o construtor de "tk.Frame" para inicializar o container.
        super().__init__(
            self.parent, # Define a janela "pai" deste Frame.
            bg = self.parent["bg"] # Define a cor de fundo para ser igual ao do pai.
        )

        # Insere o container para ser exibido em sua janela "pai", de forma centralizada.
        self.pack()

        # Inicializa o título da página.
        title = TitleLabel(
            self, # Define a janela "pai" deste título.
            text = "Calculadora de IMC" # Texto exibido no título.
        )

        # Inicializa o formulário.
        self.form = Form(
            self, # Define a janela "pai" deste formulário.
            fields = form_fields # Envia as informações para criar os campos no formulário.
        )

        # Inicializa o botão para calcular o IMC.
        button_calculate = ModelButton(
            self, # Define a janela "pai" deste botão.
            text = "Calcular", # Texto exibido no botão.
            command = self.__calculate # Ao clicar no botão, é chamada a função "calculate()".
        )
        button_calculate.pack()

        # Inicializa um Label para exibir os resultados.
        # └─ Nota de update: o ideal seria este Label abaixo também ser um "component", padronizando um único modelo para todo o projeto.
        self.label_result = tk.Label(
            self, # Define a janela "pai" deste Label.
            bg = self.parent["bg"], # Define a cor de fundo para ser igual ao do pai.

            # Configurações extras da fonte do texto.
            font = tk_font.Font(
                family = styles.FONT, # Fonte utilizada.
                size = styles.FONT_SIZE_MEDIUM, # Tamanho do texto.
            )
        )

        # Insere o Label para ser exibido em sua janela "pai", de forma centralizada.
        self.label_result.pack()


    # Método para calcular o IMC com os valores digitados no formulário.
    # └─ self: referência ao próprio objeto.
    def __calculate(self)->None:

        # Atributo para armazenar os valores obtidos do formulário.
        form_data = self.form.get_form_data()

        # O código abaixo faz uma tentativa de execução, pois como os valores dos Entries 
        # são do tipo String, a conversão para float pode falhar (ocasionando um erro).
        # └─ try: tente executar o código abaixo.
        try:

            # Obtém os valores convertidos para float.
            altura = float(form_data["altura"]) / 100.0 # Divide por 100 para obter a altura em metros.
            peso = float(form_data["peso"])

            # Cálculo do IMC.
            imc = peso / (altura * altura)

            # Atualiza o Label com o resultado.
            self.label_result["text"] = f"O seu IMC é: {imc:.1f}"
        
            # Verificação para informar se está abaixo, ideal ou acima do peso.
            # └─ o código adiciona os textos abaixo no texto que já existe no Label ("\n" pula linha).

            # IMC menor que 18.5.
            if (imc < 18.5):
                self.label_result["text"] += "\nVocê está abaixo do peso."
            # IMC maior ou igual que 18.5 e menor que 24.9.
            elif (imc >= 18.5 and imc < 24.9):
                self.label_result["text"] += "\nVocê está no peso ideal."
            # IMC maior que 24.9.
            else:
                self.label_result["text"] += "\nVocê está acima do peso."

        # └─ except: se o try não conseguir converter os valores para float, execute o código abaixo.
        except ValueError:

            # Informa o usuário com uma mensagem de erro.
            self.label_result["text"] = "Insira a altura e peso para calcular o IMC."
