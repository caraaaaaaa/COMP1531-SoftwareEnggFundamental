'''given a radius, calculate its circumference and area'''
import math

class Circle:
    '''class'''
    def __init__(self, radius):
        '''read radius of circle'''
        self.radius = radius

    def circumference(self):
        '''calculate circumference'''
        return 2 * math.pi * self.radius

    def area(self):
        '''calculate area'''
        return math.pi * self.radius * self.radius
