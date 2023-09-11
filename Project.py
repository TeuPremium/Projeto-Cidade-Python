

class Car:
    def __init__(self, id, velocidade_max):
        self.id = id    
        self.x = 0
        self.y = 0
        self.speed = 0
        self.acceleration = 0
        self.velocidade_max = velocidade_max
        self.destiny = (0,0)
        self.occupied = False 

    def limit_speed(self, new_speed):
        if new_speed <= self.velocidade_max:
            self.speed = new_speed
        else:
            self.speed =  self.velocidade_max
    
    def change_speed(self, received_speed):
        self.speed = received_speed 
    
    #Duvida_implementar_logica
    def occupy_car(self):
        self.occupied = True  

    def safe_distance(self, car2):
        distnc = car2.x - self.x
        bool = distnc >= #largura de faixa
        if bool == False:
            self.speed

    




    

class Person:

    def __init__(self, id):
        self.x = 0
        self.y = 0
        self.id = id
        self.in_car = False
        self.destiny = (0,0)

    def person_destiny(self, x, y):
        self.destino = (x,y)

    def inside_car(self):
        self.in_car = True
    
    def outside_car(self):
        self.in_car = False
