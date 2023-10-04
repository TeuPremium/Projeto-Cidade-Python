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
    def __init__(self, max_speed = 1, position = (0,0)):
        self.max_speed = max_speed
        self.car_position = position
        self.speed = (0, 0, 0)
    
    # Car position is absolute
    # Car block is relative
    def go_to(self, car_position,  coordenadas_destino: tuple, mapa : Rua, dest_block = (0,4,1)):
        linha, coluna, angle = dest_block
        a, b, angle = car_position #implementar um self
        x, y = self.car_position
        x_speed, y_speed = 0, 0
        x_destino, y_destino = coordenadas_destino
        
        # Checar se ta na posicao certa
        # if    (x-1 > mapa.tamanho * coluna + mapa.tamanho): x_speed -= 1; angle = 3
        # elif  (x+1 < mapa.tamanho * coluna + mapa.tamanho): x_speed += 1 ; angle = 1
        # if    (y-1 > mapa.tamanho * linha + mapa.tamanho): y_speed -= 1 ; angle = 2
        # elif  (y+1 < mapa.tamanho * linha + mapa.tamanho): y_speed += 1 ; angle = 0

        if(x_destino > x):
            if(x_speed <= 0):
                x_speed = 1
                angle = 1                
        elif(x_destino < x):
            if(x_speed >= 0):
                x_speed = -1
                angle = 3
        elif(y_destino > y):
            if(y_speed <= 0):
                y_speed = 1
                angle = 0
        elif(y_destino < y):
            if(y_speed >= 0):
                y_speed = - 1
                angle = 2


        self.speed = (x_speed, y_speed)    
        x+=x_speed
        y+=y_speed
        self.car_position = (x,y)

        print(x,y)
        print(x_destino, y_destino)
        # if((x_destino != x) or (y_destino != y)):
        #     self.go_to((x,y, angle), coordenadas_destino, mapa, dest_block)
        # Mudar isso para checar o angulo
        return ((x,y, angle))
    
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



    def atravessa_quarteirao(self, x_inicio, y_inicio, x_destino, y_destino):

        for linha, linha_blocos in enumerate(self.blocos):
            for coluna, bloco in enumerate(linha_blocos):
                x1, y1 = bloco
                x2, y2 = x1 + self.largura, y1 + self.largura

                if (x_inicio < x2 and x_destino > x1 and
                    y_inicio < y2 and y_destino > y1):
                    if x_inicio < x1 + (x2 - x1) / 2:
                        return (x1, y_inicio)
                    else:
                        return (x2, y_inicio)
                elif(x_inicio > x2 and x_destino < x1 and
                    y_inicio > y2 and y_destino < y1):
                    if y_inicio < y1 + (y2 - y1) / 2:
                        return (x_inicio, y1)
                    else:
                        return (x_inicio, y2)

        return False




    def definir_rota(self, carro, inicio, destino):   
        self.max = self.max +1
        x_inicio, y_inicio = inicio
        x_destino, y_destino = destino

        # retorna error se o destino = inicio
        if inicio == destino:
            raise ValueError("inicio e destino iguais")
        # retorna 0 se o destino for dentro de um bloco
        for linha, linha_blocos in enumerate(self.blocos):
            for coluna, bloco in enumerate(linha_blocos):
                x1, y1 = bloco
                x2, y2 = x1 + self.largura, y1 + self.largura
                if x1 < x_inicio < x2 and y1 < y_inicio < y2:
                    print(f'O ponto de início ({x_inicio}, {y_inicio}) está dentro do bloco ({x1}, {y1}) - ({x2}, {y2}) na linha {linha}, coluna {coluna}')
                    return 0
                if x1 < x_destino < x2 and y1 < y_destino < y2:
                    print(f'O ponto de início ({x_destino}, {y_destino}) está dentro do bloco ({x1}, {y1}) - ({x2}, {y2}) na linha {linha}, coluna {coluna}')
                    return 0
        
        

        # Obter o valor máximo de x e y a partir da última tupla
        ultimo_bloco = blocos[-1][-1]
        limite_da_cidade_x = ultimo_bloco[0] + self.largura
        limite_da_cidade_y = ultimo_bloco[1] + self.largura
        
        # o carro só deverá andar em uma única direção, que é horizontal ou vertical
        # esse if/else serve para determinar onde o carro vai parar 
        # de forma paralela ao destino final designado.
        

        if(x_inicio != destino[0]):
            
            if((limite_da_cidade_x - self.largura <= x_inicio or x_inicio <= self.largura) and
            (limite_da_cidade_x - self.largura <= x_destino or x_destino <= self.largura)):
                destino1 = (x_inicio, y_destino)
            
            else:

                destino1 = (x_destino, y_inicio)

        elif(y_inicio != destino[1]):
            if((limite_da_cidade_y - self.largura <= y_inicio <= self.largura) and
                (limite_da_cidade_y - self.largura <= y_destino <= self.largura)):

                destino1 = (x_destino, y_inicio)
            else:        

                destino1 = (x_inicio, y_destino)
        
# <------------------------------------>
        # teste para ver se o carro está atravessando algum bloco
        atravessa = self.atravessa_quarteirao(x_inicio, y_inicio, destino1[0], destino1[1])

        if (atravessa and inicio != atravessa):
            destino1 = atravessa
            self.lista_curvas.append(destino1)
            return self.definir_rota(carro, destino1, destino)
        
        
        # Verificar se destino1 está paralelo de algum bloco e ajustar conforme necessário
        for linha, linha_blocos in enumerate(self.blocos):
            for coluna, bloco in enumerate(linha_blocos):
                x1, y1 = bloco
                x2, y2 = x1 + self.largura, y1 + self.largura
                if x1 < destino1[0] < x2:
                    if(destino[0]>x1):
                        destino1 = (x1, y_inicio)
                    else:
                        destino1 = (x2, y_inicio)
                elif y1 < destino1[1] < y2:
                    if(destino[1]>y1):
                        destino1 = (x_inicio, y1)
                    else:
                        destino1 = (x_inicio, y2)


        # Verificar se destino1 está muito próximo da borda da cidade
        margem = self.largura  # Define o tamanho do quarteirão como margem de segurança
        # testa se o a coordenada vai parar fora da cidade
        if destino1[0] < margem:
            destino1 = (margem, destino1[1])

        elif destino1[0] > limite_da_cidade_x - margem:  
            destino1 = (limite_da_cidade_x - margem, destino1[1])

        if destino1[1] < margem:
            destino1 = (destino1[0], margem)

        elif destino1[1] > limite_da_cidade_y - margem:  
            destino1 = (destino1[0], limite_da_cidade_y - margem)
        
        # as vezes, o destino para de caminhar na ultima iteração e isso resolve o problema
        if(inicio == destino1):
           destino1 = (x_destino, y_destino)

        self.lista_curvas.append(destino1)
        if destino1 != destino:
            return self.definir_rota(carro, destino1, destino)
        else:
            print(self.lista_curvas)
            return self.lista_curvas



ruas = Rua()
blocos = ruas.generate_street_coordinates()
cent1 = Central_Controle(blocos, 1)

base = (4.25,0,0)

# # Exemplo de uso

largura = 4
central = Central_Controle(blocos, largura)

# Ponto de início

destino= (0,5)  # Exemplo de ponto de início
inicio = ( 21, 17)  # Exemplo de ponto de destino

rota = central.definir_rota(None, inicio, destino)
# inicio = (0,5)  # Exemplo de ponto de início
# destino = ( 16, 21)  # Exemplo de ponto de destino

carros = Carro(position=inicio)
# inicio = (4,7)
# destino = (16,7)

print(blocos)

# loop que vai movimentar o carro
for i in rota:
     base = carros.go_to(base, i, ruas)
     x,y, ang = base
     while (x,y) != i:
        ruas.draw_map([base])
        print('base: ', base)
        print('i: ',i)
        base = carros.go_to(base, i, ruas)
        x,y, ang = base


# while (1):
#     ruas.draw_map([base])
#     base = carros.go_to(base, ruas)
    