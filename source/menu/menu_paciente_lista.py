"""
Menu para listar os pacientes cadastrados no ID do nutricionista.
"""

import ttkbootstrap as ttk
from PIL import Image, ImageTk
import io

import source.styles as styles
from source.banco_dados import BancoDados
from source.component.scrollable_frame import ScrollableFrame
from source.component.title_label import TitleLabel
from source.component.form_entry import FormEntry
from source.component.model_button import ModelButton
from source.component.model_frame import ModelFrame
from source.component.model_frame import ModelFrame
from source.component.background_image_label import BackgroundImageLabel


PATH_IMAGE_PACIENTE:str = "source/image/person.png" # Caminho para a foto quando o usuário não tiver uma foto cadastrada.
PATH_ICON_PLUS:str = "source/image/plus_light.png" # Caminho para o ícone do botão de adicionar novo paciente.

class MenuPacienteLista(ttk.Frame):

    IMAGE_PACIENTE_SIZE:tuple = (160, 160) # Tamanho da foto exibida no paciente.
    FILTER_PLACEHOLDER:str = "🔍 Buscar paciente..." # Texto exibido enquanto o usuário não digitar nada.

    parent = None # Janela pai.
    open_menu = None # Método de referência para alterar de menu.
    banco_dados:BancoDados = None # Conexão com o banco de dados.

    data_pacientes = [] # Armazena os dados dos pacientes registrados no id do nutricionista.
    filter_nome:str = None # Armazena o filtro atual.

    # Salva os widgets do menu.
    input_nome:FormEntry = None
    frame_to_pacientes:ttk.Frame = None
    image_paciente_default:ImageTk.PhotoImage = None # Armazena a imagem exibida quando o paciente não tiver uma foto registrada.
    icon_plus:ttk.PhotoImage = None # Ícone exibido no botão de cadastrar novo paciente.


    # Método construtor.
    # ├─ parent: janela pai.
    # ├─ open_menu: método de referência para alterar de menu.
    # └─ banco_dados: conexão com o banco de dados.
    def __init__(self, parent, open_menu, banco_dados:BancoDados)->None:

        self.parent = parent
        self.open_menu = open_menu
        self.banco_dados = banco_dados

        # Carrega a imagem padrão para quando o paciente não tiver uma foto cadastrada.
        image = Image.open(PATH_IMAGE_PACIENTE).resize(MenuPacienteLista.IMAGE_PACIENTE_SIZE)
        self.image_paciente_default = ImageTk.PhotoImage(image)

        # Carregar o ícone para o botão de cadastrar novo paciente.
        self.icon_plus = ttk.PhotoImage(file = PATH_ICON_PLUS).subsample(4)

        # Constrói o menu.
        super().__init__(parent)
        self.pack(fill = "both", expand = True)

        # Imagem de fundo.
        self.background = BackgroundImageLabel(self, path_image = "source/image/background.png")
        self.background.place()

        # Título da página.
        title = TitleLabel(self, text = "Lista de Pacientes")
        title.pack()

        # Frame para manter todo o conteúdo da página.
        frame_content = ttk.Frame(self)
        frame_content.pack()
        frame_content.rowconfigure(1, weight = 1)

        # Input para filtrar os pacientes pelo nome.
        self.input_nome = FormEntry(frame_content, placeholder = MenuPacienteLista.FILTER_PLACEHOLDER, width = 24)
        self.input_nome.grid(row = 0, column = 0, sticky = "w", padx = styles.PADDING_MEDIUM)

        # Aplicar o filtro de nome quando perder o foco ou apertar enter.
        self.input_nome.bind("<FocusOut>", self.__apply_filter)
        self.input_nome.bind("<Return>", lambda _: self.__apply_filter())

        # Botão para navegar ao MenuPaciente.
        button_novo = ModelButton(frame_content, text = "Novo Paciente", compound = "left", image = self.icon_plus, command = lambda: self.open_menu("paciente"))
        button_novo.grid(row = 0, column = 3, sticky = "ne", padx = styles.PADDING_MEDIUM, pady = (styles.PADDING_SMALL, 0))

        # Frame de gambiarra para manter o scrollbar com a largura certa.
        self.frame_to_pacientes = ModelFrame(frame_content, width = 918, height = 99999, padding = (2, 2, 2, 2))
        self.frame_to_pacientes.grid(row = 1, column = 0, columnspan = 4, sticky = "nswe", padx = 0, pady = 0)
        self.frame_to_pacientes.pack_propagate(0) # Desabilita o redimensionamento automático.
        
        # Carrega os dados dos pacientes para exibí-los.
        self.__apply_filter()


    # Método para carregar os dados do paciente com filtros.
    def __apply_filter(self)->None:
        
        filter_nome = self.input_nome.get()
        if self.filter_nome == filter_nome:
            return
        self.filter_nome = filter_nome

        # Carrega os dados dos pacientes.
        self.data_pacientes = self.banco_dados.read(
            "paciente", # Tabela
            {
                "id_nutricionista": self.banco_dados.id_nutricionista, # Busca apenas os pacientes do nutricionista logado.
                "nome": self.filter_nome
            }
        )

        # Cria o layout para os pacientes carregados.
        self.__create_pacientes()
    

    # Método para criar o layout dos pacientes carregados.
    def __create_pacientes(self)->None:
        
        # Remove os pacientes que tinham sido carregados anteriormente.
        for child in self.frame_to_pacientes.winfo_children():
            child.destroy()
        
        # Cria o scroll para os pacientes.
        frame_scroll = ScrollableFrame(self.frame_to_pacientes, border = 1)
        frame_scroll.pack()

        # Quando não houver nenhum paciente para exibir, exibe apenas uma mensagem informativa.
        if len(self.data_pacientes) == 0:
            label = ttk.Label(
                frame_scroll,
                text = "Nenhum paciente encontrado!", 
                anchor = "center",
                font = (styles.FONT, styles.FONT_SIZE_INTERMEDIATE, "bold")
            )
            label.pack(fill = "x")
            return
        
        # Armazena as posições de cada paciente no layout de tabela.
        row:int = 0
        column:int = 0
        
        # Cria o container para cada paciente.
        for data in self.data_pacientes:
            
            container = ModelFrame(frame_scroll)
            container.grid(row = row, column = column)
            
            # Se o paciente tiver foto cadastrada, exibe ela, caso contrário, exibe a foto default.
            image = None
            if data[10]:
                image = bytes.fromhex(data[10])
                image = Image.open(io.BytesIO(image))
                image = image.resize(MenuPacienteLista.IMAGE_PACIENTE_SIZE)
                image = ImageTk.PhotoImage(image)
            else:
                image = self.image_paciente_default
            
            # Exibe a imagem do paciente.
            label_image = ttk.Label(container, image = image)
            label_image.image = image # Por alguma razão, precisa repetir a definição da imagem, caso contrário, não irá carregar do DB.
            label_image.pack()

            # Exibe o nome do paciente.
            label_nome = ttk.Label(container, text = data[2], font = (styles.FONT, styles.FONT_SIZE_MEDIUM), anchor = "center", width = 10)
            label_nome.pack(fill = "x", pady = styles.PADDING_SMALL)
            
            # Botão para acessar o perfil nutricional do paciente.
            button_perfil_nutricional = ModelButton(
                container,
                text = "Perfil Nutricional",
                command = lambda id_paciente = data[0]: self.__open_perfil_nutricional(id_paciente)
            )
            button_perfil_nutricional.pack()

            # Ao fim do loop, aumenta em 1 a posição do layout, para criar os próximos containers dos pacientes.
            column += 1
            if column > 3:
                column -= 4
                row += 1

    # Método para abrir o perfil nutricional com o id do paciente selecionado.
    def __open_perfil_nutricional(self, id_paciente:int)->None:
        
        self.banco_dados.id_paciente = id_paciente
        self.open_menu("perfil_nutricional")






































