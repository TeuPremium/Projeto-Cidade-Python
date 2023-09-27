import matplotlib.pyplot as plt
import matplotlib.patches as patches
from math import pi

class Rua:
    def __init__(self, linhas = 4, colunas = 4, tamanho = 4, carro = 1):
        self.linhas = linhas
        self.colunas = colunas
        self.quadras = (linhas + 1) * (colunas + 1)
        self.tamanho = tamanho
        self.carro = carro

    def draw_map(self, veiculos = [(4.25,0,0)]):
        _, ax = plt.subplots()
        
        # Desenhar quadras
        x, y = 0,0
        for _ in range(self.linhas):
            for _ in range(self.colunas):
                ax.add_patch(patches.Rectangle(
                    (x,y), self.tamanho, self.tamanho,
                    facecolor= 'yellow',
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

ruas = Rua()
carros = Carro()
base = (4.25,0,0)




while (1):
    ruas.draw_map([base])
    base = carros.go_to(base, ruas)
