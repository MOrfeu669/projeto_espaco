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

# Carregando e iniciando a música
pg.mixer.music.load('X2Download.com - C418_ Aria Math (128 kbps).mp3')
pg.mixer.music.play(-1)

# Definindo a fonte que será usada para renderizar o texto
font = pg.font.Font(None, 24)

# Variável para controlar o loop principal do jogo
running = True

# Definindo a fonte para o rótulo de distância
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

# Loop principal do jogo
while running:
    for event in pg.event.get():
        # Se o usuário fechar a janela ou pressionar a tecla ESC, salva os dados e termina o loop
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            save_data(star_points)
            running = False

        # Se o usuário clicar com o mouse add um ponto
        elif event.type == pg.MOUSEBUTTONDOWN:
            if tela.get_rect().collidepoint(event.pos):
                if event.button == 1:
                    # Cria uma janela tkinter invisível para a caixa de diálogo
                    root = tk.Tk()
                    root.withdraw()

                    # Solicita ao usuário o nome da estrela
                    star_name = simpledialog.askstring(
                        "Star Name", "Enter the name of the star:")
                    # Se o usuario inseriar um nome add um ponto
                    if star_name:
                        mouse_x, mouse_y = event.pos
                        star_points[star_name] = (mouse_x, mouse_y)
                # Se o clique foi com o botão direito do mouse
                elif event.button == 3:
                    mouse_x, mouse_y = event.pos
                    mouse_vector = pg.math.Vector2(mouse_x, mouse_y)

                    # Verifica se o clique foi próximo a algum marcador
                    for name, point in star_points.items():
                        marker_x, marker_y = point
                        marker_vector = pg.math.Vector2(marker_x, marker_y)
                        distance = mouse_vector.distance_to(marker_vector)
                        # Se o clique foi próximo a um marcador, remove o marcador
                        if distance < 30:
                            del star_points[name]
                            break

        elif event.type == pg.KEYDOWN:
            # Se a tecla foi F10, limpa todos os marcadores
            if event.key == pg.K_F10:
                star_points.clear()
            # Se a tecla foi F11, salva os marcadores
            elif event.key == pg.K_F11:
                save_data(star_points)
            # Se o arquivo de salvamento não existir, inicia com um dicionário vazio
            elif event.key == pg.K_F12:
                try:
                    star_points = load_data()
                except FileNotFoundError:
                    star_points = {}

    tela.blit(fundo, (0, 0))
    # Reseta o rótulo de distância
    distance_label = None
    # Obtém a posição do mouse
    mouse_x, mouse_y = pg.mouse.get_pos()
    mouse_vector = pg.math.Vector2(mouse_x, mouse_y)
    # Navega sobre os pares de pontos das estrelas
    for i, (name1, point1) in enumerate(list(star_points.items())[:-1]):
        name2, point2 = list(star_points.items())[i+1]

        # Calcula a distância do mouse até a linha entre os dois pontos
        line_start = pg.math.Vector2(point1)
        line_end = pg.math.Vector2(point2)

        # A distancia da linha for menor que 30
        line_vector = line_end - line_start
        t = max(0, min(1, (mouse_vector - line_start).dot(line_vector) /
                line_vector.length_squared()))
        projection = line_start + t * line_vector
        distance_to_line = mouse_vector.distance_to(projection)

        if distance_to_line < 30:
            # Calcula o comprimento da linha
            line_length = math.sqrt(
                (line_end.x - line_start.x) ** 2 + (line_end.y - line_start.y) ** 2)

            # Cria um rótulo com o comprimento da linha
            distance_label = distance_label_font.render(
                f"Length: {int(line_length)} px", True, (255, 255, 255))
            distance_label_pos = (mouse_x, mouse_y)
            break

    for name, point in star_points.items():
        # Obtém as coordenadas do marcador
        marker_x, marker_y = point
        # Cria um retângulo para o marcador com o centro nas coordenadas do marcador
        marker_rect = marcador.get_rect(center=(marker_x, marker_y - 9))
        # Desenha o marcador na tela
        tela.blit(marcador, marker_rect)

        # Cria uma superfície de texto com o nome da estrela
        text_surface = font.render(name, True, (255, 255, 255))
        # Desenha o nome da estrela na tela
        tela.blit(text_surface, (marker_x - 15, marker_y - 38))

    # Itera sobre os pares de pontos das estrelas
    for i, (name1, point1) in enumerate(list(star_points.items())[:-1]):
        # Obtém o próximo ponto na lista
        name2, point2 = list(star_points.items())[i+1]
        # Desenha uma linha entre os dois pontos
        pg.draw.line(tela, (255, 255, 255), point1, point2)

    # Cria uma fonte para as instruções
    instructions_font = pg.font.Font(None, 29)
    instructions_1 = instructions_font.render(
        "Botao esquerdo: adicionar marcador", True, (255, 255, 255))
    instructions_2 = instructions_font.render(
        "Botao direito: excluir marcado", True, (255, 255, 255))
    instructions_3 = instructions_font.render(
        "Tecla F10: excluir todos marcadores", True, (255, 255, 255))
    instructions_4 = instructions_font.render(
        "Tecla F11: salvar marcadores", True, (255, 255, 255))
    instructions_5 = instructions_font.render(
        "Tecla F12: carregar marcadores", True, (255, 255, 255))
    # Desenha as instruções na tela
    tela.blit(instructions_1, (10, 10))
    tela.blit(instructions_2, (10, 45))
    tela.blit(instructions_3, (10, 80))
    tela.blit(instructions_4, (10, 115))
    tela.blit(instructions_5, (10, 150))

    # Se existe um rótulo de distância, desenha-o na tela
    if distance_label:
        tela.blit(distance_label, distance_label_pos)

    pg.display.update()
    clock.tick(165)

pg.quit()
