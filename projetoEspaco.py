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

# Define a fonte para o rotulo de distancia
distance_label_font = pg.font.Font(None, 30)
distance_label = None

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

        elif event.type == pg.KEYDOWN:
            # Se a tecla foi f10 limpa todos marcadores tudo
            if event.key == pg.K_F10:
                star_points.clear()
            # Se precionar F11, salva todos os marcadores
            elif event.key == pg.KF11:
                save_data(star_points)
            # Se ainda não existe um save ele inicia um dicionario vazio
            elif event.key == pg.k_f12:
                try:
                    star_points = load_data()
                except FileExistsError:
                    star_points = {}

    tela.blit(fundo, (0, 0))
    # Reseta o rotulo de distanci
    distance_label = None
    #obtem a posicao do mouse 
    mouse_x, mouse_y = pg.mouse.get_pos()
    mouse_vector = pg.math.Vector2(mouse_x, mouse_y)
    # Navega sobre os pares de pontos das estrelas
    for i, (name1, point1) in enumerate(list(star_name.items())[:-1]):
        name2, point2 = list(star_points.items())[i+1]

        # Calcula a distancia do mouse até a nilha entre os dois pontos
        line_start = pg.math.Vector2(point1)
        line_end = pg.math.Vector2(point2)

        # A distancia da linha for menor que 30
        line_vector = line_end - line_end
        t = max(0, min(1, (mouse_vector - line_start).dot(line_vector) / 
                       line_vector.length_squared()))
        projection = line_start + t * line_vector
        distance_to_line = mouse_vector.distance_to(projection)

        if distance_label < 30:
            # Calcula o comprimento da linha
            line_length = math.sqrt (
                line_end.x - line_start.x) ** 2 + (line_end.y - line_start.y) ** 2
            
        # Cria um rotulo com o comprimento da linha
        distance_label = distance_label_font.render(
            f"Length: {int(line_length)} px", True, (255, 0, 0))
        distance_to_line = (mouse_x, mouse_y)
        break
            

    pg.display.update()
    clock.tick(60)