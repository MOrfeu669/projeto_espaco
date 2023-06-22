import pygame as pg
import tkinter as tk
from tkinter import simpledialog
import math
import os

# Inicializando o pygame e o mixer do pygame
pg.init()
pg.mixer.init()
tamanho = (1600, 1000)
tela = pg.display.set_mode(tamanho)
fundo = pg.image.load("bg.jpg")
fundo = pg.transform.scale(fundo, tamanho)
marcador = pg.image.load("wapoint.png")
clock = pg.time.Clock()

#carega e inicializa a musica
pg.mixer.music.load('X2Download.com - C418_ Aria Math (128 kbps).mp3')
pg.mixer.music.play(-1)

# Definindo a fonte que será usada para renderizar o texto
font = pg.font.Font(None, 24)

# variavel para controlar o loop principal
running = True

# Função para salvar os pontos das estrelas
def save_data(star_points, folder='save_data'):
  # Cria o diretório se ele não existir
    if not os.path.exists(folder):
        os.makedirs(folder)
    # Cria uma janela tkinter invisível para a caixa de diálogo
    root = tk.Tk()
    root.withdraw()
    # Solicita ao usuário o nome do arquivo de salvamento
    filename = simpledialog.askstring(
        "Save File", "Enter the name of the save file:")
    # Se o usuário inseriu um nome de arquivo, salva os pontos das estrelas no arquivo
    if filename:
        with open(os.path.join(folder, filename + '.txt'), 'w') as f:
            for name, point in star_points.items():
                f.write(f'{point[0]} {point[1]} {name}\n')

# Função para carregar os pontos das estrelas


def load_data(folder='save_data'):
    # Dicionário para armazenar os pontos das estrelas
    star_points = {}
    # Cria uma janela tkinter invisível para a caixa de diálogo
    root = tk.Tk()
    root.withdraw()
    # Solicita ao usuário o nome do arquivo de salvamento para carregar
    filename = simpledialog.askstring(
        "Load File", "Enter the name of the save file to load:")
    # Se o usuário inseriu um nome de arquivo, carrega os pontos das estrelas do arquivo
    if filename:
        with open(os.path.join(folder, filename + '.txt'), 'r') as f:
            for line in f:
                x, y, name = line.strip().split()
                star_points[name] = (int(x), int(y))
    return star_points


# Tentando carregar os pontos das estrelas
try:
    star_points = load_data()
except FileNotFoundError:
    # Se o arquivo de salvamento não existir, inicia com um dicionário vazio
    star_points = {}

def load_data(folder='save_data'):
    # Dicionário para armazenar os pontos das estrelas
    star_points = {}
    # Cria uma janela tkinter invisível para a caixa de diálogo
    root = tk.Tk()
    root.withdraw()
    # Solicita ao usuário o nome do arquivo de salvamento para carregar
    filename = simpledialog.askstring(
        "Load File", "Enter the name of the save file to load:")
    # Se o usuário inseriu um nome de arquivo, carrega os pontos das estrelas do arquivo
    if filename:
        with open(os.path.join(folder, filename + '.txt'), 'r') as f:
            for line in f:
                x, y, name = line.strip().split()
                star_points[name] = (int(x), int(y))
    return star_points
# carrega os pontos
try:
    star_points = load_data()
except FileNotFoundError:
    #se o arquivo de salvar não existir inicia um diconario vazio
    star_points = {}
# loop principal do jogo
while running:
    for event in pg.event.get():
        # Se o usuario fechar salva os dados e encerra o codigo
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.Key == pg.K_ESCAPE):
            save_data(star_points)
            renning = False
        
        #se o usuario clicar com o mouse add um ponto
        elif event.type == pg.MOUSEBUTTONDOWN:
            if tela.get_rect().collidepoint(event.pos):
                if event.butto == 1:
                    # cria uma janela inviseivel para a caixa de diálogo
                    root = tk.Tk()
                    root.withdraw()

                    # Solicita o usuario o nomeda estrela
                    star_name = simpledialog.askfloat(
                        "Star name", "Enter the name of the star: ")
                    # Se o usuario inserir o nome da estrela adiciona um ponto
                    if star_name:
                        mouse_x, mouse_y = event.pos
                        star_name[star_name] = (mouse_x, mouse_y)
                # Se o clique foi com o botao direito 
                elif event.button == 3:
                    mouse_x, mouse_y = event.pos
                    mouse_vector = pg.math.Vector2(mouse_x, mouse_y)

                    #verifica se o foi em algum marcador
                    for name, point in star_points.items():
                        marker_x, marker_y = point
                        marker_vector = pg.math.Vector2(marker_x, marker_y)
                        distance = mouse_vector.distance_to(marker_vector)
                        #se o clique foi em um marcador, removera o mesmo
                        if distance < 30:
                            del star_points[name]
                            break
                     

    tela.blit(fundo, (0, 0))

    pg.display.update()
    clock.tick(60)