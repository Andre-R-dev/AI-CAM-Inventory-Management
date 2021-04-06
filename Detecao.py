import tkinter
from tkinter import messagebox
from tkinter import *
from tkinter.ttk import *
import cv2
import PIL.Image, PIL.ImageTk
from PIL import Image, ImageTk
import time
import imutils
from lobe import ImageModel
import pandas as pd
import numpy as np


ex = pd.read_excel(
    "Inventario_2021.xlsx", sheet_name="Geral", header=0, na_filter=False
)


class App:
    def __init__(
        self, window, window_title, video_source=0
    ):  # por defeito a video source seria 0; #a funcao init é sempre executada no inicio
        self.window = window  # "tkinter.Tk()"
        self.window.title(window_title)
        self.video_source = video_source
        window.attributes("-fullscreen", True)  # maximiza a janela
        self.procura_por_texto = (
            0  # variavel de memoria para saber se a pesquisa foi feita por texto
        )

        # open video source (by default this will try to open the computer webcam)
        self.vid = MyVideoCapture(
            self.video_source
        )  # a funcao da captura de video fica alocada à variável vid

        # Create a canvas that can fit the above video source size
        self.canvas = tkinter.Canvas(window, width=1000, height=500, bg="white")
        self.canvas.pack()  # update à janela com as caracteristicas definidas acima

        # Button that lets the user take a snapshot
        self.btn_snapshot = tkinter.Button(
            window, text="Deteção de objeto", width=25, height=2, command=self.snapshot
        )
        self.btn_snapshot.pack(anchor=tkinter.CENTER, expand=True, side="left")

        # Button that lets the user do a search text
        self.btn_search = tkinter.Button(
            window,
            text="Procura por Texto",
            width=15,
            height=2,
            command=self.procura_texto,
        )
        self.btn_search.place(relx=0.009, rely=0.52, anchor="sw")

        # Button that lets the user close the application
        self.btn_close = tkinter.Button(
            window,
            text="Fechar Aplicação",
            width=25,
            height=2,
            command=self.close_window,
        )
        # self.btn_close.place(relx=0.8,rely=0.8, anchor='sw')
        self.btn_close.pack(anchor=tkinter.CENTER, expand=True, side="right")

        # Button to load the tensorflow model
        self.btn_load_model = tkinter.Button(
            window,
            text="Carregar Modelo",
            width=15,
            height=2,
            command=self.load_model,
        )
        self.btn_load_model.place(relx=0.9, rely=0.52, anchor="sw")
        # self.btn_load_model.pack(anchor=tkinter.CENTER, expand=True, side="right")

        # cria as labels iniciais
        self.Lbl_inicial()

        self.lista_nomes = ex["Nome"]  # lista para aparecer na entrada de texto

        # creating text box
        self.search_name.bind("<KeyRelease>", self.check_key)
        # creating list box
        self.l_box = Listbox(self.window, selectmode="BROWSE")  # criacao da listbox
        self.l_box.bind(
            "<<ListboxSelect>>", self.list_box_click
        )  # Despluta o segundo argumento quando faço clico na listbox
        self.l_box.place(relx=0.007, rely=0.45, anchor="sw")
        self.update_data(self.lista_nomes)
        #############################################################################################

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 15
        self.update()  # corre a função update

        self.window.mainloop()  # corre a janela em loop, todos os botões criados estão sempre prontos para serem carregados

    # Função para procurar o objeto por texto
    def procura_texto(self):
        if self.search_name.get() != "":
            self.obj_name = str(self.search_name.get())
            self.procura_por_texto = 1
            self.Lbl()

    # Função para fechar as janelas quando o botão é pressionado
    def close_window(self):
        self.window.destroy()

    def snapshot(self):

        # Get a frame from the video source
        ret, frame = self.vid.get_frame()

        if ret:

            # cv2.imwrite("Imagem-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
            cv2.imwrite("Imagem.png", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
            # Previsão a partir da captura realizada
            try:
                self.result = self.model.predict_from_file("Imagem.png")
                # Print top prediction
                # print(result.prediction)
                # print(result.labels[0][1]) # percentagem de certeza maior, ou seja, do result prediction

                # Print all classes
                # for label, confidence in result.labels:
                #    print(f"{label}: {confidence*100}%")
                self.obj_name = self.result.prediction
                self.Lbl()
            except:
                # caso em que não carregou o modelo
                messagebox.showinfo(
                    "Informação", "O Modelo de TensorFlow não foi carregado"
                )

    # Função para carregar o modelo de tensorflow
    def load_model(self):
        if self.dir_modelo.get() != "":
            self.model = ImageModel.load(self.dir_modelo.get())
            messagebox.showinfo(
                "Informação", "O Modelo de TensorFlow foi carregado com sucesso"
            )
        else:
            messagebox.showinfo(
                "Informação", "Insira o diretório do Modelo de TensorFlow"
            )

    # Labels iniciais
    def Lbl_inicial(self):

        """Diretorio do Modelo TensorFlow"""
        self.dir_modelo_text = tkinter.Label(
            self.window,
            text="Diretório" + "\n" + "Modelo TensorFlow",
            fg="black",
            font=("Arial", 10),
            bg="white",
            width=15,
            borderwidth=2,
            relief="groove",
        )
        self.dir_modelo_text.place(relx=0.8975, rely=0.405, anchor="sw")
        self.dir_modelo = tkinter.Entry(self.window)
        self.dir_modelo.place(relx=0.8975, rely=0.44, anchor="sw")

        # Criar as labels com os nomes do que aparece
        self.lbl_Nome_text = tkinter.Label(
            self.window,
            text="Nome",
            fg="black",
            font=("Arial", 10),
            bg="white",
            width=10,
            borderwidth=2,
            relief="groove",
        )
        self.lbl_Nome_text.place(relx=0.05, rely=0.95, anchor="sw")
        self.lbl_Quant_text = tkinter.Label(
            self.window,
            text="Quantidade",
            fg="black",
            font=("Arial", 10),
            bg="white",
            width=10,
            borderwidth=2,
            relief="groove",
        )
        self.lbl_Quant_text.place(relx=0.175, rely=0.95, anchor="sw")
        self.lbl_Sala_text = tkinter.Label(
            self.window,
            text="Sala",
            fg="black",
            font=("Arial", 10),
            bg="white",
            width=10,
            borderwidth=2,
            relief="groove",
        )
        self.lbl_Sala_text.place(relx=0.26, rely=0.95, anchor="sw")
        self.lbl_Ref_In_text = tkinter.Label(
            self.window,
            text="Ref. Int.",
            fg="black",
            font=("Arial", 10),
            bg="white",
            width=10,
            borderwidth=2,
            relief="groove",
        )
        self.lbl_Ref_In_text.place(relx=0.345, rely=0.95, anchor="sw")
        self.lbl_Ref_Ext_text = tkinter.Label(
            self.window,
            text="Ref. Ext.",
            fg="black",
            font=("Arial", 10),
            bg="white",
            width=10,
            borderwidth=2,
            relief="groove",
        )
        self.lbl_Ref_Ext_text.place(relx=0.445, rely=0.95, anchor="sw")
        self.lbl_Arm_text = tkinter.Label(
            self.window,
            text="Armário",
            fg="black",
            font=("Arial", 10),
            bg="white",
            width=10,
            borderwidth=2,
            relief="groove",
        )
        self.lbl_Arm_text.place(relx=0.55, rely=0.95, anchor="sw")
        self.lbl_Serial_text = tkinter.Label(
            self.window,
            text="Serial Number",
            fg="black",
            font=("Arial", 10),
            bg="white",
            width=15,
            borderwidth=2,
            relief="groove",
        )
        self.lbl_Serial_text.place(relx=0.68, rely=0.95, anchor="sw")
        self.lbl_Desc_text = tkinter.Label(
            self.window,
            text="Descrição",
            fg="black",
            font=("Arial", 10),
            bg="white",
            width=10,
            borderwidth=2,
            relief="groove",
        )
        self.lbl_Desc_text.place(relx=0.9, rely=0.95, anchor="sw")
        # self.lbl_Nome.pack() # coloca a label na janela, o pack() sobrepoe-se ao place, ou uso um ou outro para colocar a label

        self.lbl_Im_produto_text = tkinter.Label(
            self.window,
            text="Objeto",
            fg="black",
            font=("Arial", 10),
            bg="white",
            width=10,
            borderwidth=2,
            relief="groove",
        )
        self.lbl_Im_produto_text.place(relx=0.015, rely=0.72, anchor="sw")

        self.lbl_Certeza_text = tkinter.Label(
            self.window,
            text="Percentagem de certeza",
            fg="black",
            font=("Arial", 10),
            bg="white",
            width=20,
            borderwidth=2,
            relief="groove",
        )
        self.lbl_Certeza_text.place(relx=0.432, rely=0.825, anchor="sw")

        # Entrada de texto
        self.search_name_text = tkinter.Label(
            self.window,
            text="Procura Manual",
            fg="black",
            font=("Arial", 10),
            bg="white",
            width=12,
            borderwidth=2,
            relief="groove",
        )
        self.search_name_text.place(relx=0.0145, rely=0.17, anchor="sw")
        self.search_name = tkinter.Entry(self.window)
        self.search_name.place(relx=0.007, rely=0.2, anchor="sw")

        self.Lbl_sem_obj()

    # Label para quando não deteta nada
    def Lbl_sem_obj(self):
        self.lbl_Nome = tkinter.Label(
            self.window,
            text="Sem informação",
            fg="black",
            font=("Arial", 10),
            bg="antique white",
            width=25,
            borderwidth=2,
            relief="groove",
        )  # cria a label sobre o nome
        self.lbl_Quant = tkinter.Label(
            self.window,
            text="-",
            fg="black",
            font=("Arial", 10),
            bg="antique white",
            width=2,
            borderwidth=2,
            relief="groove",
        )  # cria a label sobre o nome
        self.lbl_Sala = tkinter.Label(
            self.window,
            text="-",
            fg="black",
            font=("Arial", 10),
            bg="antique white",
            width=4,
            borderwidth=2,
            relief="groove",
        )  # cria a label sobre o nome
        self.lbl_Ref_In = tkinter.Label(
            self.window,
            text="-",
            fg="black",
            font=("Arial", 10),
            bg="antique white",
            width=3,
            borderwidth=2,
            relief="groove",
        )  # cria a label sobre o nome
        self.lbl_Ref_Ext = tkinter.Label(
            self.window,
            text="-",
            fg="black",
            font=("Arial", 10),
            bg="antique white",
            width=15,
            borderwidth=2,
            relief="groove",
        )  # cria a label sobre o nome
        self.lbl_Arm = tkinter.Label(
            self.window,
            text="-",
            fg="black",
            font=("Arial", 10),
            bg="antique white",
            width=10,
            borderwidth=2,
            relief="groove",
        )  # cria a label sobre o nome
        self.lbl_Serial = tkinter.Label(
            self.window,
            text="Sem informação",
            fg="black",
            font=("Arial", 10),
            bg="antique white",
            width=25,
            borderwidth=2,
            relief="groove",
        )  # cria a label sobre o nome
        self.lbl_Desc = tkinter.Label(
            self.window,
            text="Sem informação",
            fg="black",
            font=("Arial", 10),
            bg="antique white",
            width=25,
            borderwidth=2,
            relief="groove",
        )  # cria a label sobre o nome
        self.lbl_Nome.place(relx=0.0, rely=0.99, anchor="sw")
        self.lbl_Quant.place(relx=0.2, rely=0.99, anchor="sw")
        self.lbl_Sala.place(relx=0.28, rely=0.99, anchor="sw")
        self.lbl_Ref_In.place(relx=0.365, rely=0.99, anchor="sw")
        self.lbl_Ref_Ext.place(relx=0.43, rely=0.99, anchor="sw")
        self.lbl_Arm.place(relx=0.55, rely=0.99, anchor="sw")
        self.lbl_Serial.place(relx=0.65, rely=0.99, anchor="sw")
        self.lbl_Desc.place(relx=0.85, rely=0.99, anchor="sw")

        # Label com a percentagem de certeza
        self.lbl_Certeza = tkinter.Label(
            self.window,
            text="0%",
            fg="black",
            font=("Arial", 10),
            bg="lemon chiffon",
            width=5,
            borderwidth=2,
            relief="groove",
        )
        self.lbl_Certeza.place(relx=0.48, rely=0.865, anchor="sw")

        # IMAGEM DEFAULT PARA O UTILIZADOR
        image_OPEN = Image.open("quadrado_vazio.png")
        image_OPEN = image_OPEN.resize((120, 120))  # downscale
        self.default_image = ImageTk.PhotoImage(image_OPEN)
        self.default_image_window = tkinter.Label(self.window, image=self.default_image)
        self.default_image_window.place(relx=0.0, rely=0.9, anchor="sw")

    # Labels para quando deteta
    def Lbl(self):
        if self.obj_name != "Nenhum_Objeto":
            # print("label")
            # print(self.obj_name)
            search = ex["Nome"].str.find(
                self.obj_name
            )  # procura pela label do objeto na tabela na coluna nome
            self.obj_name = ""  # limpar o obj_name para não acumular strings
            fnd = np.where(
                search == 0
            )  # procura no array disponibilazado da procura o valor 0 (no match = -1)
            if (
                fnd[0].size == 0
            ):  # caso em que se escreveu, mas não encontrou o objeto com esse nome
                messagebox.showinfo("Informação", "Objeto Inexistente")
            elif (
                fnd[0].size > 1
            ):  # caso em que se escreveu, mas existem vários objetos com o que foi escrito
                # procurar qual é o objeto com o nome de menor tamanho
                len_min = 100
                for i in fnd[0]:
                    len_atual = len(ex["Nome"][i])
                    if len_atual < len_min:
                        len_min = len_atual
                        min = i

                fnd = min
                self.label_com_informacao(fnd)

                messagebox.showinfo(
                    "Informação",
                    f"Poderá ser necessário que escreva de forma mais específica.\n Existem vários objectos iniciados com {self.obj_name}",
                )
            else:
                fnd = fnd[0][
                    0
                ]  # transforma o array (que normalmente só vai ter um index) num int
                self.label_com_informacao(fnd)

        else:
            self.Lbl_sem_obj()

    def label_com_informacao(self, fnd):

        rowData = ex.loc[fnd, :]  # a informação toda do objeto

        self.lbl_Nome = tkinter.Label(
            self.window,
            text=rowData[1],
            fg="black",
            font=("Arial", 10),
            bg="antique white",
            width=25,
            borderwidth=2,
            relief="groove",
        )  # cria a label sobre o nome
        self.lbl_Quant = tkinter.Label(
            self.window,
            text=rowData[2],
            fg="black",
            font=("Arial", 10),
            bg="antique white",
            width=2,
            borderwidth=2,
            relief="groove",
        )  # cria a label sobre o nome
        self.lbl_Sala = tkinter.Label(
            self.window,
            text=rowData[3],
            fg="black",
            font=("Arial", 10),
            bg="antique white",
            width=4,
            borderwidth=2,
            relief="groove",
        )  # cria a label sobre o nome
        self.lbl_Ref_In = tkinter.Label(
            self.window,
            text=rowData[4],
            fg="black",
            font=("Arial", 10),
            bg="antique white",
            width=3,
            borderwidth=2,
            relief="groove",
        )  # cria a label sobre o nome
        self.lbl_Ref_Ext = tkinter.Label(
            self.window,
            text=rowData[5],
            fg="black",
            font=("Arial", 10),
            bg="antique white",
            width=15,
            borderwidth=2,
            relief="groove",
        )  # cria a label sobre o nome
        self.lbl_Arm = tkinter.Label(
            self.window,
            text=rowData[6],
            fg="black",
            font=("Arial", 10),
            bg="antique white",
            width=10,
            borderwidth=2,
            relief="groove",
        )  # cria a label sobre o nome
        self.lbl_Serial = tkinter.Label(
            self.window,
            text=rowData[7],
            fg="black",
            font=("Arial", 10),
            bg="antique white",
            width=25,
            borderwidth=2,
            relief="groove",
        )  # cria a label sobre o nome
        self.lbl_Desc = tkinter.Label(
            self.window,
            text=rowData[8],
            fg="black",
            font=("Arial", 10),
            bg="antique white",
            width=25,
            borderwidth=2,
            relief="groove",
        )  # cria a label sobre o nome

        self.lbl_Nome.place(relx=0.0, rely=0.99, anchor="sw")
        self.lbl_Quant.place(relx=0.2, rely=0.99, anchor="sw")
        self.lbl_Sala.place(relx=0.28, rely=0.99, anchor="sw")
        self.lbl_Ref_In.place(relx=0.365, rely=0.99, anchor="sw")
        self.lbl_Ref_Ext.place(relx=0.43, rely=0.99, anchor="sw")
        self.lbl_Arm.place(relx=0.55, rely=0.99, anchor="sw")
        self.lbl_Serial.place(relx=0.65, rely=0.99, anchor="sw")
        self.lbl_Desc.place(relx=0.85, rely=0.99, anchor="sw")
        if self.procura_por_texto == 0:
            # Label com a percentagem de certeza
            self.lbl_Certeza = tkinter.Label(
                self.window,
                text=str(int(self.result.labels[0][1] * 100)) + "%",
                fg="black",
                font=("Arial", 10),
                bg="lemon chiffon",
                width=5,
                borderwidth=2,
                relief="groove",
            )
            self.lbl_Certeza.place(relx=0.48, rely=0.865, anchor="sw")
        else:
            self.procura_por_texto = 0
            # Label com a percentagem de certeza
            self.lbl_Certeza = tkinter.Label(
                self.window,
                text="-",
                fg="black",
                font=("Arial", 10),
                bg="lemon chiffon",
                width=5,
                borderwidth=2,
                relief="groove",
            )
            self.lbl_Certeza.place(relx=0.48, rely=0.865, anchor="sw")

        # IMAGEM DEFAULT PARA O UTILIZADOR
        image_OPEN = Image.open(rowData[0])
        image_OPEN = image_OPEN.resize((120, 120))  # downscale
        self.default_image = ImageTk.PhotoImage(image_OPEN)
        self.default_image_window = tkinter.Label(self.window, image=self.default_image)
        self.default_image_window.place(relx=0.0, rely=0.9, anchor="sw")

    # update da janela
    def update(self):
        # Get a frame from the video source
        (
            ret,
            frame,
        ) = self.vid.get_frame()  # função get_frame abaixo onde capturamos o video

        if ret:
            self.photo = PIL.ImageTk.PhotoImage(
                image=PIL.Image.fromarray(frame)
            )  # criação da imagem a ir para a janela
            self.canvas.create_image(
                500, 250, image=self.photo, anchor=tkinter.CENTER
            )  # criação e posicionamento da imagem na janela

        self.window.after(
            self.delay, self.update
        )  # apos 15ms corre a funcao update, ou seja, fica aqui em loop. A cada 15 ms atualiza a imagem

    ###########################   AUTO COMPLETE   #############################################################
    # Verifica o que está escrito no search_name
    # Function for checking the key pressed and updating the listbox
    def check_key(self, event):

        nome_inserido = str(self.search_name.get())
        # print(value)

        # get data from l
        if nome_inserido == "":
            dados = self.lista_nomes
        else:
            dados = []
            for item in self.lista_nomes:
                if nome_inserido.lower() in item.lower():
                    dados.append(item)

        # update data in listbox
        self.update_data(dados)

    # funcao update data in listbox
    def update_data(self, dados):
        # clear prevdata data
        self.l_box.delete(0, "end")
        # put new data
        for item in dados:
            self.l_box.insert("end", item)

    #############################################################################################

    ############################### PASSAR DA LISTBOX PARA O INPUT DE TEXTO ###########################################
    def list_box_click(self, event):
        # print("Hello")
        self.obj_name = self.l_box.get(ANCHOR)
        self.search_name.delete(
            0, "end"
        )  # eliminar o que foi escrito na entrada de texto
        self.search_name.insert(0, self.obj_name)  # inserir o que foi selecionado
        # print(self.obj_name)
        # print(self.l_box.get(self.l_box.curselection()))


class MyVideoCapture:
    def __init__(self, video_source=0):
        # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        # Get video source width and height
        codec = 0x47504A4D  # MJPG
        self.fps = self.vid.set(cv2.CAP_PROP_FPS, 30.0)
        self.codec = self.vid.set(cv2.CAP_PROP_FOURCC, codec)
        self.width = self.vid.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        self.height = self.vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        # self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        # self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_frame(self):
        if self.vid.isOpened():  # só corre se tiver a janela aberta
            ret, frame = self.vid.read()
            frame = imutils.resize(frame, width=960)  # downscale
            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (ret, None)

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()
            cv2.destroyAllWindows()


# Create a window and pass it to the Application object
App(tkinter.Tk(), "Informação Inventário")
