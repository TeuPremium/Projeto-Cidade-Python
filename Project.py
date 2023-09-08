class Car:
     """Class representing a car"""
    def __init__(self, x_pos : int, y_pos : int):
        self.x = x_pos
        self.y = y_pos
        self.speed = 0
        self.acceleration = 2

    def move(x_pos : int, y_pos : int):
        pass

    def change_speed():
        pass
class Person:
     """Class representing a person"""
    def __init__(self, x_pos : int, y_pos : int):
        self.x = x_pos
        self.y = y_pos

    def call(self):
        pass


class Lane:
     """Class representing a lane"""
    def __init__(self, orientation, corner1, corner2, width):
        self.corner1 = corner1
        self.corner2 = corner2   
        self.corner_left_bottom  = False
        self.corner_left_top = False
        self.corner_right_bottom = False
        self.corner_right_top = False
        self.orientation = orientation
        self.width = width

class Street:
     """Class representing a street"""
    def __init__(self, lane_width = 1, city_length= 10, city_height = 10, total_lanes = 3):
        self.number = False
        self.max_speed = False
        self.lanes = total_lanes
        self.city_length = city_length
        self.city_height = city_height
        self.lane_width = lane_width
        
    def calculate_corners(self,):
        self.corner = [0,1]

class MQTT:
     """Class importing and executing mqtt"""
    def __init__(self):
        pass