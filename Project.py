import matplotlib.pyplot as plt

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
    def __init__(self, lane_width=1, city_length=20, city_height=20, streets=4, margin =2):
        self.number = False
        self.max_speed = False
        self.streets = streets
        self.city_length = city_length
        self.city_height = city_height
        self.lane_width = lane_width
        self.margin = margin
        self.horizontal_streets =  []
        self.vertical_streets =  []

    def calculate_streets(self):
        # padding = self.margin
        # width = self.lane_width

        # horizontal_streets = self.horizontal_streets
        # vertical_streets = self.vertical_streets

        # city_length = self.city_length
        # city_height = self.city_height

        # v_gap = city_height - 2*padding #gap between horizontal streets
        # h_gap = city_length - 2*padding #gap between vertical streets

        
        # # para facilitar, eu separei as ruas horizontais e verticais
        # # está sujeito a mudanças, mas imagino que facilite para plotar
        # horizontal_streets.append([ 0 , padding,
        #                             0, padding + width, 
        #                             city_length, padding,
        #                             city_length, padding + width]) #rua de baixo
        # horizontal_streets.append([ 0 , padding,
        #                             0, padding + width*2, 
        #                             city_length, padding,
        #                             city_length, padding + width*2]) #rua de baixo
        # # coordenadas da rua (x, y, x, y, x, y, x, y, orientation**)
        # # cantos inferiores esquerdo e direito e cantos superiores esquerdo e direito respectivamente

        # vertical_streets.append([   padding , 0 ,
        #                             padding + width, 0,
        #                             padding ,city_height,
        #                             padding + width, city_height]) #rua de baixo
        # vertical_streets.append([   padding , 0 ,
        #                             padding + width*2, 0,
        #                             padding ,city_height,
        #                             padding + width*2, city_height]) #rua de baixo

        # vertical_start = v_gap + padding + width
        # horizontal_start = h_gap + padding + width
        # for _ in range(self.streets - 1):
        #     horizontal_streets.append([ 0 , padding,
        #                                 0, padding + width, 
        #                                 city_length, padding,
        #                                 city_length, padding + width])
        #     horizontal_streets.append([ 0 , padding,
        #                                 0, padding + width*2, 
        #                                 city_length, padding,
        #                                 city_length, padding + width*2]) #rua de baixo
            
        #     vertical_streets.append([   padding , 0 ,
        #                                 padding + width, 0,
        #                                 padding ,city_height,
        #                                 padding + width, city_height])
        #     vertical_streets.append([   padding , 0 ,
        #                                 padding + width*2, 0,
        #                                 padding ,city_height,
        #                                 padding + width*2, city_height]) #rua de baixo
            
        #     vertical_start += v_gap + width
        #     horizontal_start += h_gap + width

            
        # print(horizontal_streets)
        # # create_horizontal_street = generate_street("h", self.lane_width, )
        # # print(create_horizontal_street)
        # # create_street = generate_street("v", self.lane_width)
        # # print(create_street)

            padding = self.margin
            lane_width = self.lane_width
            street_width = 2 * lane_width  # Total width of the street (two lanes)

            horizontal_streets = self.horizontal_streets
            vertical_streets = self.vertical_streets

            city_length = self.city_length
            city_height = self.city_height

            # 
            if((((self.streets * self.lane_width*2) + padding*2)>city_height) or (((self.streets * self.lane_width*2) + padding*2)>city_length)):
                print((self.streets * self.lane_width*2) + padding*2)
                print(city_height)
                raise ValueError()

            # Calculates the space between streets based on the distance from the sides
            # and the given street width
            v_gap = (city_height - (2 * padding + street_width )) / (self.streets -1) 
            h_gap = (city_length - (2 * padding + street_width))  / (self.streets -1)
            
            
            # Coordinates for the first horizontal street
            horizontal_streets.append([0, padding, city_length, padding])
            horizontal_streets.append([0, padding + street_width, city_length, padding + street_width])
            # Coordinates for the first vertical street
            vertical_streets.append([ padding,0,padding,  city_height])
            vertical_streets.append([ padding + street_width,0, padding + street_width,  city_height])

            # Calculate the gap between streets
            street_gap = v_gap / (self.streets - 1)

            for i in range(1, self.streets):
                y = padding + i * v_gap
                x = padding + i * h_gap
                horizontal_streets.append([0, y, city_length, y])
                horizontal_streets.append([0, y + street_width, city_length, y + street_width])

                vertical_streets.append([ x,0,x,  city_height])
                vertical_streets.append([ x + street_width,0, x + street_width,  city_height])



    def plot_streets(self):
        plt.figure(figsize=(self.city_length, self.city_height))

        for i, h_street_coords in enumerate(self.horizontal_streets):
            plt.plot(h_street_coords[::2], h_street_coords[1::2], color='black')
   
        for i, v_street_coords in enumerate(self.vertical_streets):
            plt.plot(v_street_coords[::2], v_street_coords[1::2], color='black')
        

        plt.xlim(0, self.city_length)
        plt.ylim(0, self.city_height)

        plt.gca().set_aspect('equal', adjustable='box')
        plt.show()


    def generate_street(self, orientation, width):
        self.corner_left_bottom = False
        self.corner_left_top = False
        self.corner_right_bottom = False
        self.corner_right_top = False
        self.orientation = orientation
        self.width = width

p = city()
p.calculate_streets()
p.plot_streets()




class MQTT:
    def __init__(self):
        pass
