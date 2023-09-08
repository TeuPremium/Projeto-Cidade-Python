class Car:
    def __init__(self, x_pos: int, y_pos: int):
        self.x = x_pos
        self.y = y_pos
        self.speed = 0
        self.acceleration = 2

    def move(x_pos: int, y_pos: int):
        pass

    def change_speed():
        pass


class Person:
    def __init__(self, x_pos: int, y_pos: int):
        self.x = x_pos
        self.y = y_pos

    def call(self):
        pass


# separar cidade em uma lista com duas listas de ruas
# rua como uma lista com 2 faixas
# faixa como uma lista com as posicoes ocupadas ou vazias

# ===== versus =====

# cidade como uma grande matriz com todas as localizações
# ruas como marcações nas cidades
# 0 para vazio
# 1 para rua para indice ++
# 2 para indice --
# +4 para carros parados
# +8 para pessoas esperando carros
# +16 para carros trafegando na rua

# ==== versus ===
# ruas vão ter suas coordenadas minimas e máximas (4 cantos)
# ruas vão ter suas intercessões
class street:
    def __init__(self, orientation, width):
        self.corner_left_bottom = False
        self.corner_left_top = False
        self.corner_right_bottom = False
        self.corner_right_top = False
        self.orientation = orientation
        self.width = width
        

    
class city:
    def __init__(self, lane_width=1, city_length=10, city_height=10, streets=3, margin = 1):
        self.number = False
        self.max_speed = False
        self.streets = streets
        self.city_length = city_length
        self.city_height = city_height
        self.lane_width = lane_width
        self.margin = margin

    def calculate_h_streets(self):
        horizontal_streets = []
        vertical_streets = []
        padding = self.margin
        width = self.width
        city_length = self.city_length
        city_height = self.city_height
        
        # para facilitar, eu separei as ruas horizontais e verticais
        # está sujeito a mudanças, mas imagino que facilite para plotar
        horizontal_streets.append([ 0 , padding,
                                    0, padding + width, 
                                    city_length, padding,
                                    city_length, padding + width]) #rua de baixo
        # coordenadas da rua (x, y, x, y, x, y, x, y)
        # cantos inferiores esquerdo e direito e cantos superiores esquerdo e direito respectivamente

        vertical_streets.append([ padding , 0 ,
                                     padding + width, 0,
                                    padding ,city_height,
                                     padding + width, city_height]) #rua de baixo

        for _ in range(self.streets - 1):
            horizontal_streets.append()
            vertical_streets.append()
            

        create_horizontal_street = generate_street("h", self.lane_width)
        print(create_horizontal_street)
        create_street = generate_street("v", self.lane_width)
        print(create_street)
        
    pass

    def generate_street(self, orientation, width):
        self.corner_left_bottom = False
        self.corner_left_top = False
        self.corner_right_bottom = False
        self.corner_right_top = False
        self.orientation = orientation
        self.width = width

p = city()
p.calculate_h_streets()





class MQTT:
    def __init__(self):
        pass
