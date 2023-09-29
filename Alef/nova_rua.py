import matplotlib.pyplot as plt
import matplotlib.patches as patches
from math import pi

class Rua:
    def __init__(self, linhas = 4, colunas = 4, tamanho = 4, carro = 1, limite_velocidade = 10):
        self.linhas = linhas
        self.colunas = colunas
        self.quadras = (linhas + 1) * (colunas + 1)
        self.tamanho = tamanho
        self.carro = carro
        self.blocos = [[None for _ in range(colunas)] for _ in range(linhas )]

    def generate_street_coordinates(self):
        x, y = 0, 0
        for linha in range(self.linhas):
            for coluna in range(self.colunas):
                self.blocos[linha][coluna] = (x, y)
                x += self.carro * 2 + self.tamanho
            y += self.carro * 2 + self.tamanho
            x = 0

        return self.blocos

    def is_block_free(self, linha, coluna):
        if self.blocos[linha][coluna] is not None:
            return True
        else:
            return False
        
    def draw_map(self, veiculos = [(4.25,0,0)]):
        _, ax = plt.subplots()
        
        # Desenhar quadras
        x, y = 0,0
        for linha in range(self.linhas):
            for coluna in range(self.colunas):
                # self.blocos[linha][coluna] = (x, y)
                ax.add_patch(patches.Rectangle(
                    (x,y), self.tamanho, self.tamanho,
                    facecolor= 'orange',
                    edgecolor= 'black',
                    fill=True
                ))

                x += self.carro * 2 + self.tamanho
            y += self.carro * 2 + self.tamanho
            x = 0
        
        # Desenhar veiculos
        # A posicao de cada um deve ser marcada em outro lugar antes de enviar
        for x,y, angle in veiculos:
            if (angle == 0): posicoes = [[x,y],[x,y+0.75],[x+0.25,y+1],[x+0.5,y+0.75],[x+0.5,y]]
            elif (angle == 1): posicoes = [[x,y],[x+0.75,y],[x+1,y-0.25],[x+0.75,y-0.5],[x,y-0.5]]
            elif (angle == 2): posicoes = [[x,y],[x,y-0.75],[x+0.25,y-1],[x+0.5,y-0.75],[x+0.5,y]]
            else: posicoes = [[x,y],[x-0.75,y],[x-1,y-0.25],[x-0.75,y-0.5],[x,y-0.5]]

            ax.add_patch(patches.Polygon(
                posicoes,
                closed=True,
                fill=True,
                facecolor='red'
            ))

        
        # Mostrar todas as ruas e etc.
        ax.set_xlim(-self.carro*2,(self.carro * 2 + self.tamanho)*(self.linhas))
        ax.set_ylim(-self.carro*2,(self.carro * 2 + self.tamanho)*(self.colunas))
        
        # Definir um evento para fechar
        plt.show()

class Carro():
    def __init__(self, max_speed = 1):
        self.max_speed = max_speed
    
    # Car position is absolute
    # Car block is relative
    def go_to(self, car_position, mapa : Rua, dest_block = (0,4,1)):
        linha, coluna, angle = dest_block
        x, y, angle = car_position
        x_speed, y_speed = 0, 0
        
        # Checar se ta na posicao certa
        if    (x-1 > mapa.tamanho * coluna + mapa.tamanho): x_speed -= 1; angle = 3
        elif  (x+1 < mapa.tamanho * coluna + mapa.tamanho): x_speed += 1 ; angle = 1
        if    (y-1 > mapa.tamanho * linha + mapa.tamanho): y_speed -= 1 ; angle = 2
        elif  (y+1 < mapa.tamanho * linha + mapa.tamanho): y_speed += 1 ; angle = 0
        
        # Mudar isso para checar o angulo
        return (x+x_speed, y+y_speed, angle)
    
    def get_current_block(self, car_position, mapa: Rua):
        x, y, _ = car_position
        linha = int(y // mapa.tamanho)
        coluna = int(x // mapa.tamanho)
        return linha, coluna
    
   


class Central_Controle():
    def __init__(self, blocos, largura_bloco = 4):
        self.blocos = blocos
        self.largura = largura_bloco

    def definir_rota(self, carro, inicio, destino):
        x_inicio, y_inicio = inicio
        x_destino, y_destino = destino

        
        for linha, linha_blocos in enumerate(self.blocos):
            for coluna, bloco in enumerate(linha_blocos):
                x1, y1 = bloco
                x2, y2 = x1 + self.largura, y1 + self.largura

                if x1 <= x_inicio <= x2 and y1 <= y_inicio <= y2:
                    return 0
                    raise Exception(f'O ponto de início ({x_inicio}, {y_inicio}) está dentro do bloco ({x1}, {y1}) - ({x2}, {y2}) na linha {linha}, coluna {coluna}')
                
                if x1 <= x_destino <= x2 and y1 <= y_destino <= y2:
                    return 0
                    raise Exception(f'O ponto de início ({x_destino}, {y_destino}) está dentro do bloco ({x1}, {y1}) - ({x2}, {y2}) na linha {linha}, coluna {coluna}')

        if(x_inicio<=self.largura):
            destino1 = (x_inicio, y_destino)

        else:
            destino1 = (x_destino, y_inicio)


        # # se destino1 está dentro de um bloco, terá coordenadas ajustadas
        # for linha, linha_blocos in enumerate(self.blocos):
        #     for coluna, bloco in enumerate(linha_blocos):
        #         x1, y1 = bloco
        #         x2, y2 = x1 + self.largura, y1 + self.largura
        #         if x1 <= destino1[0] <= x2 and y1 <= destino1[1] <= y2:
        #             destino1 = (x2, destino1[1])

# <------------------------------------_>

        ultimo_bloco = blocos[-1][-1]

        # Obter o valor máximo de x e y a partir da última tupla
        limite_da_cidade_x = ultimo_bloco[0] + self.largura
        limite_da_cidade_y = ultimo_bloco[1] + self.largura

        # Verificar se destino1 está muito próximo da borda da cidade
        margem = self.largura  # Define a margem de segurança
        if destino1[0] < margem:
            destino1 = (margem, destino1[1])
        elif destino1[0] > limite_da_cidade_x - margem:  
            destino1 = (limite_da_cidade_x - margem, destino1[1])

        if destino1[1] < margem:
            destino1 = (destino1[0], margem)
        elif destino1[1] > limite_da_cidade_y - margem:  
            destino1 = (destino1[0], limite_da_cidade_y - margem)

        # Verificar se destino1 está dentro de algum bloco e ajustar conforme necessário
        for linha, linha_blocos in enumerate(self.blocos):
            for coluna, bloco in enumerate(linha_blocos):
                x1, y1 = bloco
                x2, y2 = x1 + self.largura, y1 + self.largura

                if x1 <= destino1[0] <= x2 and y1 <= destino1[1] <= y2:
                    if abs(destino1[0] - x1) < abs(destino1[0] - x2):
                        destino1 = (x1, destino1[1])
                    else:
                        destino1 = (x2, destino1[1])

                    if abs(destino1[1] - y1) < abs(destino1[1] - y2):
                        destino1 = (destino1[0], y1)
                    else:
                        destino1 = (destino1[0], y2)
        print(destino1)



        



ruas = Rua()
blocos = ruas.generate_street_coordinates()
carros = Carro()
cent1 = Central_Controle(blocos, 1)

# base = (4.25,0,0)
# print(blocos)
# while (1):
#     ruas.draw_map([base])
#     base = carros.go_to(base, ruas)
    
# # Exemplo de uso
largura = 4

central = Central_Controle(blocos, largura)

# Ponto de início
inicio = (5,5)  # Exemplo de ponto de início
destino = (11, 11)  # Exemplo de ponto de destino

central.definir_rota(None, inicio, destino)
