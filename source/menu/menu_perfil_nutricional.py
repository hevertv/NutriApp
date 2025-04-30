"""
Menu para exibir o perfil nutricional do paciente.
Nota: por falta de tempo, acabei fazendo rápido e deixei tudo um pouco bagunçado, porém da para melhorar este código.
"""

import ttkbootstrap as ttk
from PIL import Image, ImageTk
import io
from datetime import datetime
import math
from tkinter import filedialog
import json


import source.styles as styles
from source.banco_dados import BancoDados
from source.toast import Toast
from source.component.model_frame import ModelFrame
from source.component.model_button import ModelButton
from source.component.background_image_label import BackgroundImageLabel
from source.component.scrollable_frame import ScrollableFrame


PATH_BACKGROUND:str = "source/image/background.png" # Armazena o caminho para a imagem de fundo.
PATH_IMAGE_PACIENTE:str = "source/image/person.png" # Caminho para a foto quando o usuário não tiver uma foto cadastrada.
PATH_IMC:str = "source/image/imc.png" # Caminho para a imagem do imc.
PATH_ICON_EXPORT:str = "source/image/export_light.png" # Caminho para o ícone de exportar os dados.
PATH_ICON_PLUS:str = "source/image/plus_light.png" # Caminho para o ícone do botão de adicionar novo paciente.
PATH_ICON_VIEW:str = "source/image/view_light.png" # Caminho para o ícone de visualizar.
PATH_ICON_PHONE:str = "source/image/phone_dark.png" # Caminho para o ícone de contato.

class MenuPerfilNutricional(ttk.Frame):

    IMAGE_TOP_SIZE:tuple = (96, 96) # Tamanho das fotos exibidas no topo.
    
    parent = None # Janela pai.
    open_menu = None # Método de referência para alterar de menu.
    banco_dados:BancoDados = None # Conexão com o banco de dados.

    # Armazena os dados do paciente.
    data_paciente = None
    data_anamnese = None
    data_antropometria = None
    data_inquerito_alimentar = None

    # Salva os widgets do menu.
    image_paciente_default:ImageTk.PhotoImage = None # Armazena a imagem exibida quando o paciente não tiver uma foto registrada.
    image_imc:ImageTk.PhotoImage = None # Armazena a imagem do imc.
    image_export:ImageTk.PhotoImage = None # Armazena o ícone do botão de exportar dados.
    image_plus:ImageTk.PhotoImage = None # Armazena o ícone dos botões de cadastras.
    image_view:ImageTk.PhotoImage = None # Armazena o ícone do botão de visualizar.
    image_phone:ImageTk.PhotoImage = None # Armazena o ícone para os contatos do paciente.

    # Método construtor.
    # ├─ parent: janela pai.
    # ├─ open_menu: método de referência para alterar de menu.
    # └─ banco_dados: conexão com o banco de dados.
    def __init__(self, parent, open_menu, banco_dados:BancoDados)->None:
        
        self.parent = parent
        self.open_menu = open_menu
        self.banco_dados = banco_dados

        # Antes de tudo, carrega os dados do paciente.
        self.data_paciente = self.banco_dados.ready_by_id("paciente", id_name = "id_paciente", id_value = self.banco_dados.id_paciente)
        self.data_anamnese = self.banco_dados.ready_by_id("anamnese", id_name = "id_paciente", id_value = self.banco_dados.id_paciente)
        self.data_antropometria = self.banco_dados.ready_by_id("antropometria", id_name = "id_paciente", id_value = self.banco_dados.id_paciente)
        self.data_inquerito_alimentar = self.banco_dados.ready_by_id("inquerito_alimentar", id_name = "id_paciente", id_value = self.banco_dados.id_paciente)

        # Constrói o menu.
        super().__init__(parent)
        self.pack(fill = "both", expand = True)
        self.columnconfigure((1, 2, 3), weight = 1)
        self.columnconfigure((0, 4), weight = 2)

        # Cria a imagem de fundo.
        menu_background = BackgroundImageLabel(self, PATH_BACKGROUND)
        menu_background.place()

        # Carrega a imagem padrão para quando o paciente não tiver uma foto cadastrada.
        image = Image.open(PATH_IMAGE_PACIENTE).resize(MenuPerfilNutricional.IMAGE_TOP_SIZE)
        self.image_paciente_default = ImageTk.PhotoImage(image)

        # Carrega a imagem do imc.
        image = Image.open(PATH_IMC).resize(MenuPerfilNutricional.IMAGE_TOP_SIZE)
        self.image_imc = ImageTk.PhotoImage(image)

        # Carregar o ícone para os contatos do paciente.
        image = Image.open(PATH_ICON_PHONE).resize(MenuPerfilNutricional.IMAGE_TOP_SIZE)
        self.image_phone = ImageTk.PhotoImage(image)

        # Carrega o ícone de export.
        image = Image.open(PATH_ICON_EXPORT).resize((16, 16))
        self.image_export = ImageTk.PhotoImage(image)

        # Carregar o ícone para os botões de cadastrar.
        image = Image.open(PATH_ICON_PLUS).resize((16, 16))
        self.image_plus = ImageTk.PhotoImage(image)

        # Carregar o ícone para o botão de visualizar os formulários.
        image = Image.open(PATH_ICON_VIEW).resize((16, 16))
        self.image_view = ImageTk.PhotoImage(image)

        # Cria a parte superior do menu.
        self.__create_top()

        # Cria a parte central do menu.
        self.__create_center()


    # Método apenas para criar o topo do menu.
    def __create_top(self)->None:

        # Frame para a parte superior da tela.
        frame_top = ModelFrame(self, bootstyle = "light", relief = "raised")
        frame_top.grid(row = 0, column = 0, columnspan = 5, sticky = "nswe", padx = 0, pady = (0, styles.PADDING_LARGE))
        frame_top.columnconfigure(3, weight = 1)

        # Frame para informações do paciente.
        frame_paciente = ModelFrame(frame_top, padding = 2)
        frame_paciente.grid(row = 0, column = 0)
        
        # Exibe a imagem do paciente.
        image = None
        if self.data_paciente[10]:
            image = bytes.fromhex(self.data_paciente[10])
            image = Image.open(io.BytesIO(image))
            image = image.resize(MenuPerfilNutricional.IMAGE_TOP_SIZE)
            image = ImageTk.PhotoImage(image)
        else:
            image = self.image_paciente_default
        label_image_paciente = ttk.Label(frame_paciente, image = image)
        label_image_paciente.image = image # Por alguma razão, precisa repetir a definição da imagem, caso contrário, não irá carregar do DB.
        label_image_paciente.grid(row = 0, column = 0)
        
        frame_paciente_inner = ttk.Frame(frame_paciente, padding = (styles.PADDING_SMALL, styles.PADDING_MEDIUM))
        frame_paciente_inner.grid(row = 0, column = 1, sticky = "nswe")

        label_nome = ttk.Label(frame_paciente_inner, text = self.data_paciente[2], font = (styles.FONT, styles.FONT_SIZE_MEDIUM, "bold"), width = 17, anchor = "w")
        label_nome.pack(fill = "x")
        
        # Calcula a idade.
        data_atual = datetime.now()
        data_nascimento = datetime.strptime(self.data_paciente[6], "%d/%m/%Y")
        idade = data_atual.year - data_nascimento.year
        if data_atual.month < data_nascimento.month or (data_atual.month == data_nascimento.month and data_atual.day < data_nascimento.day):
            idade -= 1
        label_idade = ttk.Label(frame_paciente_inner, text = str(idade) + " anos", font = (styles.FONT, styles.FONT_SIZE_MEDIUM), anchor = "w")
        label_idade.pack(fill = "x")

        label_sexo = ttk.Label(frame_paciente_inner, text = self.data_paciente[7], font = (styles.FONT, styles.FONT_SIZE_MEDIUM), anchor = "w")
        label_sexo.pack(fill = "x")

        # Frame para as informações do imc.
        frame_imc = ModelFrame(frame_top, padding = 2)
        frame_imc.grid(row = 0, column = 1)

        # Exibe a imagem do container.
        label_image = ttk.Label(frame_imc, image = self.image_imc)
        label_image.grid(row = 0, column = 0)

        frame_imc_inner = ttk.Frame(frame_imc, padding = (styles.PADDING_SMALL, styles.PADDING_MEDIUM))
        frame_imc_inner.grid(row = 0, column = 1, sticky = "nswe")

        if self.data_antropometria:

            peso = self.data_antropometria[1]
            altura = float(self.data_antropometria[2] / 100)
            imc = math.floor(peso / (altura ** 2) * 10) / 10
            
            imc_result = ""
            if imc < 18.5:
                imc_result = "Peso Baixo"
            elif imc <= 24.9:
                imc_result = "Peso Normal"
            elif imc <= 29.9:
                imc_result = "Sobrepeso"
            elif imc <= 34.9:
                imc_result = "Obesidade I"
            elif imc <= 39.9:
                imc_result = "Obesidade II (severa)"
            else:
                imc_result = "Obesidade III (mórbida)"

            label_imc_result = ttk.Label(frame_imc_inner, text = imc_result, font = (styles.FONT, styles.FONT_SIZE_MEDIUM, "bold"), width = 17, anchor = "w")
            label_imc_result.pack()

            label_imc = ttk.Label(frame_imc_inner, text = imc, font = (styles.FONT, styles.FONT_SIZE_MEDIUM), anchor = "w")
            label_imc.pack(fill = "x")

            label_peso_altura = ttk.Label(frame_imc_inner, text = str(peso) + " kg - " + str(altura) + " m", font = (styles.FONT, styles.FONT_SIZE_MEDIUM), anchor = "w")
            label_peso_altura.pack(fill = "x")

        else:
            label_informativo = ttk.Label(frame_imc_inner, text = "Sem registro", font = (styles.FONT, styles.FONT_SIZE_MEDIUM), width = 17, anchor = "center")
            label_informativo.pack(expand = True)

        # Frame para informações de contato.
        frame_contato = ModelFrame(frame_top, padding = 2)
        frame_contato.grid(row = 0, column = 2)

        # Exibe a imagem de contato.
        label_image = ttk.Label(frame_contato, image = self.image_phone)
        label_image.grid(row = 0, column = 0)

        frame_contato_inner = ttk.Frame(frame_contato, padding = (styles.PADDING_SMALL, styles.PADDING_MEDIUM))
        frame_contato_inner.grid(row = 0, column = 1, sticky = "nswe")

        label_contato = ttk.Label(frame_contato_inner, text = "Contatos", font = (styles.FONT, styles.FONT_SIZE_MEDIUM, "bold"), width = 17, anchor = "w")
        label_contato.pack()
        
        label_telefone = ttk.Label(frame_contato_inner, 
                                   text = "(" + self.data_paciente[4][0:2] + ") " + self.data_paciente[4][3:len(self.data_paciente) - 1],
                                   font = (styles.FONT, styles.FONT_SIZE_MEDIUM), anchor = "w")
        label_telefone.pack(fill = "x")

        label_email = ttk.Label(frame_contato_inner, text = self.data_paciente[3], font = (styles.FONT, styles.FONT_SIZE_MEDIUM), width = 17, anchor = "w")
        label_email.pack(fill = "x")

        button_export = ModelButton(frame_top, text = "Exportar Dados", compound = "left", cursor = "hand2", image = self.image_export, command = self.__export_data)
        button_export.grid(row = 0, column = 3, sticky = "se", padx = styles.PADDING_MEDIUM, pady = styles.PADDING_MEDIUM)


    # Método para criar o conteúdo central.
    def __create_center(self)->None:

        # Frame para a anamnese.
        frame_anamnese = ModelFrame(self, width = 200, height = 275, padding = 2)
        frame_anamnese.grid(row = 1, column = 1)
        frame_anamnese.pack_propagate(0) # Desabilita o redimensionamento automático.
        
        label_anamnese = ttk.Label(frame_anamnese, text = "Anamnese", font = (styles.FONT, styles.FONT_SIZE_MEDIUM, "bold"), bootstyle = "light-inverse", anchor = "center", padding = styles.PADDING_SMALL)
        label_anamnese.pack(fill = "x")

        frame_anamnese_inner = ttk.Frame(frame_anamnese, padding = styles.PADDING_SMALL)
        frame_anamnese_inner.pack(fill = "both", expand = True)
        
        if self.data_anamnese:
            frame_anamnese_inner.columnconfigure((0, 1), weight = 1)
            label_info = ttk.Label(frame_anamnese_inner, text = "Data: " + self.data_anamnese[10], font = (styles.FONT, styles.FONT_SIZE_MEDIUM))
            label_info.grid(row = 0, column = 0)
            button_view = ModelButton(frame_anamnese_inner, bootstyle = "info", text = "", image = self.image_view, command = lambda: Toast.warning("O sistema para visualizar não foi implementado."))
            button_view.grid(row = 0, column = 1, sticky = "e")
        else:
            label_info = ttk.Label(frame_anamnese_inner, text = "Nenhum registro.", anchor = "center", font = (styles.FONT, styles.FONT_SIZE_SMALL))
            label_info.pack(fill = "both", expand = True)

        button_anamnese = ModelButton(frame_anamnese, text = "Adicionar", compound = "left", image = self.image_plus, command = lambda: self.open_menu("anamnese"))
        button_anamnese.pack(fill = "x", padx = 0, pady = 0)
    

        # Frame para a antropometria.
        frame_antropometria = ModelFrame(self, width = 200, height = 275, padding = 2)
        frame_antropometria.grid(row = 1, column = 2)
        frame_antropometria.pack_propagate(0) # Desabilita o redimensionamento automático.
        
        label_antropometria = ttk.Label(frame_antropometria, text = "Antropometria", font = (styles.FONT, styles.FONT_SIZE_MEDIUM, "bold"), bootstyle = "light-inverse", anchor = "center", padding = styles.PADDING_SMALL)
        label_antropometria.pack(fill = "x")

        frame_antropometria_inner = ttk.Frame(frame_antropometria, padding = styles.PADDING_SMALL)
        frame_antropometria_inner.pack(fill = "both", expand = True)
        
        if self.data_antropometria:
            frame_antropometria_inner.columnconfigure((0, 1), weight = 1)
            label_info = ttk.Label(frame_antropometria_inner, text = "Data: " + self.data_antropometria[5], font = (styles.FONT, styles.FONT_SIZE_MEDIUM))
            label_info.grid(row = 0, column = 0)
            button_view = ModelButton(frame_antropometria_inner, bootstyle = "info", text = "", image = self.image_view, command = lambda: Toast.warning("O sistema para visualizar não foi implementado."))
            button_view.grid(row = 0, column = 1, sticky = "e")
        else:
            label_info = ttk.Label(frame_antropometria_inner, text = "Nenhum registro.", anchor = "center", font = (styles.FONT, styles.FONT_SIZE_SMALL))
            label_info.pack(fill = "both", expand = True)

        button_antropometria = ModelButton(frame_antropometria, text = "Adicionar", compound = "left", image = self.image_plus, command = lambda: self.open_menu("antropometria"))
        button_antropometria.pack(fill = "x", padx = 0, pady = 0)


        # Frame para o inquerito alimentar.
        frame_inquerito_alimentar = ModelFrame(self, width = 200, height = 275, padding = 2)
        frame_inquerito_alimentar.grid(row = 1, column = 3)
        frame_inquerito_alimentar.pack_propagate(0) # Desabilita o redimensionamento automático.
        
        label_inquerito_alimentar = ttk.Label(frame_inquerito_alimentar, text = "Inquerito Alimentar", font = (styles.FONT, styles.FONT_SIZE_MEDIUM, "bold"), bootstyle = "light-inverse", anchor = "center", padding = styles.PADDING_SMALL)
        label_inquerito_alimentar.pack(fill = "x")

        frame_inquerito_alimentar_inner = ttk.Frame(frame_inquerito_alimentar, padding = styles.PADDING_SMALL)
        frame_inquerito_alimentar_inner.pack(fill = "both", expand = True)

        if self.data_inquerito_alimentar:
            frame_inquerito_alimentar_inner.columnconfigure((0, 1), weight = 1)
            label_info = ttk.Label(frame_inquerito_alimentar_inner, text = "Data: " + self.data_inquerito_alimentar[15], font = (styles.FONT, styles.FONT_SIZE_MEDIUM))
            label_info.grid(row = 0, column = 0)
            button_view = ModelButton(frame_inquerito_alimentar_inner, bootstyle = "info", text = "", image = self.image_view, command = lambda: Toast.warning("O sistema para visualizar não foi implementado."))
            button_view.grid(row = 0, column = 1, sticky = "e")
        else:
            label_info = ttk.Label(frame_inquerito_alimentar_inner, text = "Nenhum registro.", anchor = "center", font = (styles.FONT, styles.FONT_SIZE_SMALL))
            label_info.pack(fill = "both", expand = True)

        button_inquerito_alimentar = ModelButton(frame_inquerito_alimentar, text = "Adicionar", compound = "left", image = self.image_plus, command = lambda: self.open_menu("inquerito_alimentar"))
        button_inquerito_alimentar.pack(fill = "x", padx = 0, pady = 0)
    

    # Método para exportar os dados do paciente.
    def __export_data(self)->None:

        filename = filedialog.asksaveasfilename(defaultextension = "paciente.json", filetypes = [("Arquivos JSON", "*.json")], title = "Exportar dados do paciente")

        if filename:
            data = {
                "nome": self.data_paciente[2],
                "email": self.data_paciente[3],
                "telefone": self.data_paciente[4],
                "estado_civil": self.data_paciente[5],
                "data_nascimento": self.data_paciente[6],
                "sexo": self.data_paciente[7],
                "raca": self.data_paciente[8],
                "naturalidade": self.data_paciente[9],
                "data_criacao": self.data_paciente[11]
            }

            if self.data_anamnese:
                data["anamnese"] = {
                    "religiao": self.data_anamnese[1],
                    "profissao": self.data_anamnese[2],
                    "tabagismo": self.data_anamnese[3],
                    "etilismo": self.data_anamnese[4],
                    "atividade_fisica": self.data_anamnese[5],
                    "reside_social": self.data_anamnese[6],
                    "questoes_religiosas": self.data_anamnese[7],
                    "historia_familiar": self.data_anamnese[8]
                }

            if self.data_antropometria:
                data["antropometria"] = {
                    "peso": self.data_antropometria[1],
                    "altura": self.data_antropometria[2],
                    "circunferencia_cintura": self.data_antropometria[3],
                    "composicao_corporal": self.data_antropometria[4]
                }
            
            if self.data_inquerito_alimentar:
                data["inquerito_alimentar"] = {
                    "desjejum": self.data_inquerito_alimentar[1],
                    "desjejum_horario": self.data_inquerito_alimentar[2],
                    "lanche_manha": self.data_inquerito_alimentar[3],
                    "lancha_manha_horario": self.data_inquerito_alimentar[4],
                    "almoco": self.data_inquerito_alimentar[5],
                    "almoco_horario": self.data_inquerito_alimentar[6],
                    "lanche_tarde": self.data_inquerito_alimentar[7],
                    "lanche_tarde_horario": self.data_inquerito_alimentar[8],
                    "jantar": self.data_inquerito_alimentar[9],
                    "jantar_horario": self.data_inquerito_alimentar[10],
                    "ceia": self.data_inquerito_alimentar[11],
                    "ceia_horario": self.data_inquerito_alimentar[12],
                    "outras": self.data_inquerito_alimentar[13],
                    "outras_horario": self.data_inquerito_alimentar[14]
                }

            with open(filename, "w") as file:
                json.dump(data, file, indent = 4)
            
            Toast.success("Dados do paciente exportados.")







