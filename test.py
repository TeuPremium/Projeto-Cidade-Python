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
        self.lista_curvas = []
        self.blocos = blocos
        self.largura = largura_bloco
        self.max = 0

    def is_interval_intersecting_block(self, x_inicio, y_inicio, x_destino, y_destino):
        for linha, linha_blocos in enumerate(self.blocos):
            for coluna, bloco in enumerate(linha_blocos):
                x1, y1 = bloco
                x2, y2 = x1 + self.largura, y1 + self.largura

                if (x_inicio < x2 and x_destino > x1 and
                    y_inicio < y2 and y_destino > y1):
                    return True

        return False
    
    def definir_rota(self, inicio, destino):
        x_inicio, y_inicio = inicio
        x_destino, y_destino = destino

        # Check if the route intersects any blocks
        if self.is_interval_intersecting_block(x_inicio, y_inicio, x_destino, y_destino):
            # If there's an intersection, try to find an alternative route
            if x_inicio != x_destino:
                destino1 = (x_inicio, y_destino)
            else:
                destino1 = (x_destino, y_inicio)
            
            # Check if the alternative route also intersects blocks
            if self.is_interval_intersecting_block(x_inicio, y_inicio, destino1[0], destino1[1]):
                raise ValueError("Cannot find a clear route")
        else:
            # If there's no intersection, use the original destination
            destino1 = destino

        # Add the intermediate point to the route
        self.lista_curvas.append(destino1)
        print(self.lista_curvas)
        if destino1 != destino:
            return self.definir_rota(destino1, destino)
        else:
            return self.lista_curvas




ruas = Rua()
blocos = ruas.generate_street_coordinates()
carros = Carro(1)
cent1 = Central_Controle(blocos, 1)

base = (4.25,0,0)

# while (1):
    # ruas.draw_map([base])
    # base = carros.go_to(base, ruas)
    
# # Exemplo de uso
largura = 4

central = Central_Controle(blocos, largura)

# Ponto de início
inicio = (0,5)  # Exemplo de ponto de início
destino = (21,16)  # Exemplo de ponto de destino

central.definir_rota( inicio, destino)
