from HpAPI import HpAPI
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from io import BytesIO
import requests
from datetime import datetime
import customtkinter as ctk
import os

app = ctk.CTk()
app.title("Personagens de Harry Potter")

label_text = tk.Label(app, text="")
label_text.pack()

label_img = tk.Label(app)
label_img.pack()

def carregaApp(casa_hogwarts = ''):
    carregaInfosApi(casa_hogwarts)
    carregaPersonagens()

def carregaInfosApi(casa_hogwarts):

    global resposta_api, quantidade_personagens, labels_opcoes, cores_casa, casas_disponiveis, contador

    hp_api = HpAPI(casa_hogwarts)
    casas_disponiveis = HpAPI().getCasasDisponiveis()
    cores_casa = hp_api.getCoresCasa()
    resposta_api = hp_api.getPersonagens()
    quantidade_personagens = hp_api.quantidadePersonagens()

    contador = 0

    labels_opcoes = [label for label, value in casas_disponiveis]

def setaCoresApp(bg, fg):
    app.configure(fg_color=bg)
    label_text.configure(bg=f"{bg}", fg=f"{fg}")
    label_img.configure(bg=f"{bg}", fg=f"{fg}")
    ctk.set_default_color_theme('blue')

def carregaPersonagens():
    setaCoresApp(cores_casa['bg'], cores_casa['fg'])
    atualizaPersonagem()

def geraInfos(personagem):

    tem_data = False
    if personagem['dateOfBirth']:
        tem_data = True
        data_nascimento = datetime.strptime(personagem['dateOfBirth'], "%d-%m-%Y")
        data_nascimento = data_nascimento.strftime("%d/%m/%Y")

    generos = {
        'male': 'Masculino',
        'female': 'Feminino'
    }

    infos = {
        'Nome': personagem['name'] if personagem['name'] else 'Não informado',
        'Data de Nascimento': data_nascimento if tem_data else 'Não informado',
        'Casa': personagem['house'] if personagem['house'] else 'Não informado',
        'Patrono': personagem['patronus'] if personagem['patronus'] else 'Não informado',
        'Ator': personagem['actor'] if personagem['actor'] else 'Não informado',
        'Gênero': generos[personagem['gender']] if personagem['gender'] else 'Não informado',
        'Vivo': 'Sim' if personagem['alive'] else 'Não',
    }

    temp = f"Personagem {contador+1} de {quantidade_personagens+1}\n\n"
    for key, value in infos.items():
        temp += f"{key}: {value}\n"
    return temp

def atualizaPersonagem():

    personagem = resposta_api[contador]
    
    info = geraInfos(personagem)
    label_text.config(text=info)
    
    imagem_url = personagem['image']

    if imagem_url:
        img_data = requests.get(imagem_url).content
        img = Image.open(BytesIO(img_data))
    else:
        diretorio_imagem = os.path.join(os.path.dirname(__file__), 'imagens/nada_encontrado.png')
        img = Image.open(diretorio_imagem)

    img = img.resize((163, 227))
    img_tk = ImageTk.PhotoImage(img)
    label_img.config(image=img_tk)
    label_img.image = img_tk

def proximo():
    global contador
    if contador < quantidade_personagens - 1:
        contador += 1
        atualizaPersonagem()

def anterior():
    global contador
    if contador > 0:
        contador -= 1
        atualizaPersonagem()

def selecionaCasa(event):    
    label_selecionada = combo.get()
    valor_da_label = next((v for l, v in casas_disponiveis if l == label_selecionada), '')
    carregaApp(valor_da_label)

carregaApp()

combo = ttk.Combobox(app, values=labels_opcoes)
combo.set("Selecione a casa")
combo.pack(pady=10)
combo.bind("<<ComboboxSelected>>", selecionaCasa)

btn_ant = tk.Button(app, text="Anterior", command=anterior)
btn_ant.pack(side="left", padx=20, pady=10)

btn_prox = tk.Button(app, text="Próximo", command=proximo)
btn_prox.pack(side="right", padx=20, pady=10)

app.mainloop()
