"""
Menu de login de usuário
"""


import ttkbootstrap as ttk
import numpy as np
import json

import source.styles as styles
from source.banco_dados import BancoDados
from source.pattern import Pattern
from source.toast import Toast
from source.component.form_entry import FormEntry
from source.component.form_label import FormLabel
from source.component.model_button import ModelButton
from source.component.model_frame import ModelFrame
from source.component.background_image_label import BackgroundImageLabel


PATH_BACKGROUND = "source/image/login_background.png" # Armazena o caminho para a imagem de fundo.
PATH_USER_DATA = "data/user_data.json" # Caminho do arquivo que armazena o login/senha do usuário.
    

class MenuLogin(ttk.Frame):

    parent = None # Janela pai.
    open_menu = None # Atributo para o método de referência para alterar de menu.
    banco_dados:BancoDados = None # Conexão com o banco de dados.
    animation_jump:bool = False # Define quando o usuário quer pular a animação do logotipo.
    animation_started:bool = False # Define o momento que a animação tiver sido iniciada (apenas para evitar a chamada da animação 2x).

    # Salva os widgets do menu.
    input_email:FormEntry = None
    input_senha:FormEntry = None
    frame_information:ttk.Frame = None
    background:BackgroundImageLabel = None
    logotype:ttk.Label = None


    # Método construtor.
    # ├─ parent: janela pai.
    # ├─ open_menu: método de referência para alterar de menu.
    # └─ banco_dados: conexão com o banco de dados.
    def __init__(self, parent, open_menu, banco_dados:BancoDados)->None:

        self.parent = parent
        self.open_menu = open_menu
        self.banco_dados = banco_dados

        # Constrói o menu.
        super().__init__(self.parent)
        self.pack(fill = "both", expand = True)
        
        # Imagem de fundo.
        self.background = BackgroundImageLabel(self, path_image = PATH_BACKGROUND)
        self.background.place()

        # Frame para inserir as informações.
        self.frame_information = ttk.Frame(self, padding = (styles.PADDING_LARGE, 0), width = 520)
        self.frame_information.pack(fill = "y", side = "right")
        self.frame_information.pack_propagate(0) # Desabilita o redimensionamento automático.

        # Cria o logotipo.
        self.__create_logotype()

        # Caso o usuário já tenha feito login alguma vez, tenta fazer login automático, se não, inicia normalmente.
        def login_auto()->None:
            if not self.__login_auto():
                
                # Cria a animação após um determinado tempo, caso a animação não tenha sido cancelada.
                self.after(
                    1000,
                    lambda: (
                        setattr(self, "animation_started", True),
                        self.__animate_logotype() if not self.animation_jump else None
                    )
                )
                
                # Detecta quando o usuário clicar com o botão esquerdo do mouse para pular a animação.
                self.bind_all(
                    "<Button-1>",
                    lambda _: (
                        setattr(self, "animation_jump", True), # Altera o atributo para pular a animação.
                        self.unbind_all("<Button-1>"), # Para de detectar o clique do mouse.
                        self.__animate_logotype() if not self.animation_started else None # Apenas para não chamar o método de animação 2x, quando a animação já tiver sido chamada anteriormente.
                    )
                )
        self.after(350, login_auto) # Gambiarra: espera um tempo apenas para não bugar, pois o App precisa do retorno do método construtor antes de mudar de tela (coisa)


    # Método para criar o logotipo.
    def __create_logotype(self)->None:
        self.logotype = ttk.Label(
            self.frame_information, # Janel pai.
            text = "NutriApp", # Texto.
            font = (styles.FONT_LOGOTYPE, styles.FONT_SIZE_GIANT, "bold") # Configurações de fonte.
        )
        self.logotype.place(relx = 0.5, rely = 0.5, anchor = "center")


    # Método para criar a animação do logotipo.
    # ├─ x: Eixo x, utilizado para calcular o y.
    # ├─ y: Eixo y, define a posição y do logotipo.
    # └─ y_lower_value: armazena a menor posição de y.
    def __animate_logotype(self, x:float = 0, y:float = 0.5, y_lower_value = 0.5)->None:

        # A animação é criada por uma função matemática que cria um desenho de onda.
        # Link para a visualização do gráfico: https://www.desmos.com/calculator/8ccflhkba9
        # ├─ Quando x = 0, y = 0.5
        # └─ Quando x ≃ 2.5, y ≃ 0.2

        # Calcula a posição de y.
        x += 0.026 # Somar um valor menor deixa a animação mais rápida.
        y = 0.15 * np.sin((4 * np.pi * x / 10) + np.pi / 2) + 0.35

        # Se a direção de y começar a inverter ou a animação tenha sido pulada, pare a animação na posição final.
        if y > y_lower_value or self.animation_jump:
            self.animation_jump = True
            self.logotype.place(relx = 0.5, rely = 0.2, anchor = "center")
            self.logotype.update()
            self.__create_form_login() # Cria o formulário de login.
            return

        # Se não, reposiciona o logotipo com as novas coordenadas.
        self.logotype.place(relx = 0.5, rely = y, anchor = "center")
        self.logotype.update()

        # Aguarda um tempo para continuar a animação.
        self.logotype.after(7, lambda: self.__animate_logotype(x, y, y))


    # Método para criar o formulário de login.
    def __create_form_login(self)->None:

        # Container para o formulário.
        frame_form = ModelFrame(self.frame_information)
        frame_form.place(relx = 0.5, rely = 0.5, anchor = "center", width = 324)
        frame_form.columnconfigure((0, 1), weight = 1) # Configura para que as colunas possuam a mesma largura.

        # Cria os componentes para o formulário.
        label_email = FormLabel(frame_form, text = "E-mail")
        label_email.grid(row = 0, column = 0)
        self.input_email = FormEntry(frame_form, pattern = Pattern.EMAIL, warning_message = "Insira um e-mail válido")
        self.input_email.grid(row = 1, column = 0, columnspan = 2)

        label_senha = FormLabel(frame_form, text = "Senha")
        label_senha.grid(row = 2, column = 0)
        self.input_senha = FormEntry(frame_form, is_password = True)
        self.input_senha.grid(row = 3, column = 0, columnspan = 2)

        # Botões internos.
        button_criar_conta = ModelButton(frame_form, text = "Criar conta", bootstyle = "primary-link", command = lambda: self.open_menu("nutricionista"))
        button_criar_conta.grid(row = 4, column = 0, sticky = "w")
        button_entrar = ModelButton(frame_form, text = "Entrar", command = lambda: self.__login(email = self.input_email.get(), senha = self.input_senha.get()))
        button_entrar.grid(row = 4, column = 1, sticky = "ew")

        # Botão fora do layout.
        button_esqueceu_senha = ModelButton(
            self.frame_information, 
            text = "Esqueceu sua senha?", 
            bootstyle = "info-link", 
            command = lambda: Toast.warning("O sistema para a recuperação de senha ainda não foi implementado.")
        )
        button_esqueceu_senha.place(relx = 0.5, rely = 0.72, anchor = "center")

        # Isto corrige a ordem de seleção no formulário através da tecla TAB.
        self.input_email.lift()
        self.input_senha.lift()
        button_entrar.lift()
        button_criar_conta.lift()

        # Foca o input quando o usuário visualizar pela primeira vez.
        self.input_email.focus()

        # Possibilita fazer o login ao pressionar a tecla "Enter", se estiver selecionado nos inputs.
        self.input_email.bind("<Return>", lambda _: self.__login(email = self.input_email.get(), senha = self.input_senha.get()))
        self.input_senha.bind("<Return>", lambda _: self.__login(email = self.input_email.get(), senha = self.input_senha.get()))


    # Método para fazer login ao clicar no botão.
    def __login(self, email:str, senha:str, save_login:bool = True)->bool:

        validate_login = self.banco_dados.get_user_auth(email = email, senha = senha)
        if validate_login:
            
            # Salva os dados de login do usuário, para fazer o login automático nas próximas vezes.
            if save_login:
                try:
                    with open(PATH_USER_DATA, "w") as file_opened:
                        data = {"email": email, "senha": senha}
                        json.dump(data, file_opened)
                except OSError as _:
                    pass

            # Altera de tela.
            Toast.info("Seja bem vindo(a).")
            self.open_menu("paciente_lista")
            return True
        
        Toast.danger("Email e/ou senha não cadastrados.")
        return False


    # Método para fazer login automaticamente ao iniciar.
    def __login_auto(self)->bool:
        
        # Tentar ler os dados do usuário, caso existam.
        try:
            with open(PATH_USER_DATA, "r") as file_opened:
                data_file = file_opened.read()

                # Verifica se os dados são um JSON válido.
                try:
                    data = json.loads(data_file)

                    # Se tudo estiver certo, faz login automático.
                    if "email" in data and "senha" in data:
                        if self.__login(email = data["email"], senha = data["senha"]):
                            return True
                        else:
                            return False
                    else:
                        print("Erro: o arquivo JSON não está com os campos corretos para fazer login automático.")
                
                # Os dados no arquivo são inválidos.
                except json.JSONDecodeError as error:
                    print(f"Erro: formato JSON inválido. {error}")
        
        # Detecta algum problema na leitura.
        except OSError as error:
            pass
        
        return False