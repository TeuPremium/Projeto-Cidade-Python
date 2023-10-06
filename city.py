import matplotlib.pyplot as plt
import matplotlib.patches as patches
from math import pi
import random

# Escolha o numero de veiculos e pessoas alterando
# o valor de pares para a quantidade desejada:
Pares = 10

# Define a classe quadra que representa um bloco na cidade
class quadra: # OK
    def __init__(self, x, y, tamanho = 4):
        # b = baixo, e = esquerda, c = cima, d = direita
        self.b_e = (x,y)  # Canto inferior esquerdo
        self.b_d = (x + tamanho, y)  # Canto inferior direito
        self.c_e = (x, y + tamanho)  # Canto superior esquerdo
        self.c_d = (x + tamanho, y + tamanho)  # Canto superior direito
        # Spawn de pessoa
        # define os pontos de aparecimento das pessoas
        self.spawn_people= ((x+tamanho/2,y+tamanho), (x+tamanho,y+tamanho/2),
                             (x+tamanho/2,y), (x,y+tamanho/2))

# Define a classe Person que representa uma pessoa na cidade
class Person:  # OK
    # recebe o quarteirao e o tamanho dele, para gerar uma pessoa situada nele
    def __init__(self, rua, tamanho):
        # Gera posição inicial e final aleatória para a pessoa
        self.inicial,self.d_i = self.generate_random_position(rua, tamanho)
        self.final,self.d_f = self.generate_random_position(rua, tamanho)

        # Define a posição atual, direção e se a pessoa foi pega
        self.position, self.d = self.inicial, self.d_i
        self.pego = False

    # Gera uma posição aleatória para a pessoa na quadra
    def generate_random_position(self, rua, tamanho):
        # Gerar direcao
        pos = random.randint(0, 3)
        # match (pos):
        #     case 0: value = rua.b_e
        #     case 1: value = rua.b_d
        #     case 2: value = rua.c_e
        #     case 3: value = rua.c_d

        return rua.spawn_people[pos], pos

    # Atualiza a posição inicial, final e direção da pessoa
    def update_new(self, rua, tamanho):
        self.inicial,self.d_i = self.generate_random_position(rua, tamanho)
        self.final,self.d_f = self.generate_random_position(rua, tamanho)
        # Position atual
        self.position, self.d = self.inicial, self.d_i
        self.pego = False

# Define a classe 'Rua' que representa uma rua na cidade 
class Rua: #ok
    def __init__(self, tamanho = 4, carro = 1):
        self.linhas  = tamanho
        self.colunas = tamanho
        self.tamanho = tamanho
        self.carro   = carro
        self.blocos : list[list[quadra]] = [[None for _ in range(tamanho)] for _ in range(tamanho )]
    
    # Gera as coordenadas das quadras que compõem a rua
    def generate_street_coordinates(self):
        x, y = 2, 2
        for linha in range(self.linhas):
            for coluna in range(self.colunas):
                self.blocos[linha][coluna] = quadra(x, y)
                x += self.carro * 2 + self.tamanho
            y += self.carro * 2 + self.tamanho
            x = 2
        return self.blocos
    
     # Gera pessoas aleatórias na cidade
    def generate_random_people(self, num_people):
        people = []
        for _ in range(num_people):
            x = random.randint(0, self.tamanho-1)
            y = random.randint(0, self.tamanho-1)
            person = Person(self.blocos[x][y], self.tamanho)
            people.append(person)
        return people
    
    # Desenha o mapa da cidade
    def draw_map(self, veiculos = [(4.25,0,0)], people=None):
        fig, ax = plt.subplots()
        
        # Desenhar quadras
        for linha in range(self.linhas):
            for coluna in range(self.colunas):
                # self.blocos[linha][coluna] = (x, y)
                ax.add_patch(patches.Rectangle(
                    self.blocos[linha][coluna].b_e, self.tamanho, self.tamanho,
                    facecolor= 'orange',
                    edgecolor= 'black',
                    fill=True
                ))
        
        #gerar pessoas
        if people:
            for person in people:
                x, y = person.position
                color = 'blue' if (not person.pego) else 'green'
                # print(color)
                ax.add_patch(patches.Circle(
                    (x, y), 0.3,  # Adjust the circle size as needed
                    fill=True,
                    facecolor= color
                )) 

        # Gerar veiculos
        for x,y, angle,_ in veiculos:
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
        ax.set_xlim(0,(self.carro * 2 + self.tamanho)*(self.linhas) + self.carro*2)
        ax.set_ylim(0,(self.carro * 2 + self.tamanho)*(self.colunas) + self.carro*2)
        
        # Definir um evento para fechar
        mng = plt.get_current_fig_manager()
        mng.window.geometry()
        mng.resize(500,500)
        plt.show(block=False)
        plt.pause(0.2)
        plt.close()

# Define a classe Central de Controle que gerencia o tráfego e os carros
class Central_Controle():
    def __init__(self, blocos, novos_carros = 1, largura_bloco = 4, ):
        self.lista_curvas = []
        self.blocos = blocos
        self.largura = largura_bloco
        # Criar novos carros
        self.carros = []
        for _ in range(novos_carros):
            x,y = random.randint(0,len(blocos)-1),random.randint(0,len(blocos)-1)
            x,y = blocos[x][y].spawn_people[0]
            self.carros.append((x, y + 1,1, True)) # Mudança na ultima

    # Verifica se um carro atravessa um quarteirão por dentro
    def atravessa_quarteirao(self, x_inicio, y_inicio, x_destino, y_destino):
        for linha, linha_blocos in enumerate(self.blocos):
            for coluna, bloco in enumerate(linha_blocos):
                x1, y1 = bloco
                x2, y2 = x1 + self.largura, y1 + self.largura

                if (x_inicio < x2 and x_destino > x1 and
                    y_inicio < y2 and y_destino > y1):
                    if x_inicio < x1 + (x2 - x1) / 2:   return (x1, y_inicio)
                    else:                               return (x2, y_inicio)
                elif(x_inicio > x2 and x_destino < x1 and
                    y_inicio > y2 and y_destino < y1):
                    if y_inicio < y1 + (y2 - y1) / 2:   return (x_inicio, y1)
                    else:                               return (x_inicio, y2)

        return False

    # Atualiza a posição dos carros e o movimento das pessoas
    def update(self, pessoas, ruas, tamanho = 4):
        # Ir para cada um
        for i, carro in enumerate(self.carros):
            x_car, y_car, angulo, mudanca = self.carros[i]
            alvo, direcao = pessoas[i].position, pessoas[i].d
            y_speed, x_speed = 0,0

            # Descobrir a rua certa
            if (direcao == 0): # Cima
                x_pessoa = alvo[0]
                y_pessoa = alvo[1] + 1
            elif(direcao == 1): # direita
                x_pessoa = alvo[0] + 1
                y_pessoa = alvo[1]
            elif(direcao == 2): # baixo
                x_pessoa = alvo[0]
                y_pessoa = alvo[1] - 1
            else:              # esquerda
                x_pessoa = alvo[0] - 1
                y_pessoa = alvo[1]

            # Fazer o movimento
            if (x_car < x_pessoa):      x_speed = 1
            elif (x_car > x_pessoa):    x_speed = -1
            if (y_car < y_pessoa):    y_speed = 1
            elif (y_car > y_pessoa):    y_speed = -1

            # Mudar a direcao do carro
            
            # Ver se tá no lugar da pessoa para trocar
            if (x_car == x_pessoa and y_pessoa == y_car):
                pessoas[i].position = pessoas[i].final
                pessoas[i].d = pessoas[i].d_f
                if (not pessoas[i].pego): pessoas[i].pego = True
                else: 
                    aleatorio_x, aleatorio_y = random.randint(0, tamanho-1),random.randint(0, tamanho-1)
                    pessoas[i].update_new(ruas[aleatorio_x][aleatorio_y], tamanho)

            # Chacar se esta em uma rua
            teste_x = int(x_car % (tamanho + 2)); teste_y = int(y_car % (tamanho + 2))
            if ((teste_y in [0,1,2]) or (not mudanca)): 
                # Continuar na mesma direcao se travar
                x_car += x_speed 
                if (x_speed > 0): angulo = 1; mudar = True
                elif (x_speed < 0): angulo = 3; mudar = True
                
            if ((teste_x in [0,1,2]) or (not mudanca)): 
                # Continuar na mesma direcao se travar
                y_car += y_speed
                if (y_speed > 0): angulo = 0; mudar = True
                elif (y_speed < 0): angulo = 2; mudar = True
                

            self.carros[i] = (x_car, y_car, angulo, mudanca)

            print(f"Posicao Carro: {x_car},{y_car} e {teste_y},{teste_x} com {x_speed},{y_speed}; Posicao pessoa:{x_pessoa},{y_pessoa}, {angulo=} {mudanca}")

            
        

# Inicializa a geração da cidade e carros
ruas = Rua()
blocos = ruas.generate_street_coordinates()

people = ruas.generate_random_people(PARES)
central = Central_Controle(blocos, PARES) # Define os carros

# Loop principal para desenhar a cidade e atualizar o movimento
while True:
    ruas.draw_map(central.carros , people)
    central.update(people, blocos)
