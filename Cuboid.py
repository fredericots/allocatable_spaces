from Rectangle import Rectangle
from Segment import Segment

class Cuboid:
    
    def __init__(self, cuboid_json):
        
        self.id = cuboid_json['id']
        xi = cuboid_json['x']['start']
        xf = cuboid_json['x']['end']
        zi = cuboid_json['z']['start']
        zf = cuboid_json['z']['end']
        
        self.rect = Rectangle(xi, xf, zi, zf)
        
        self.yi = cuboid_json['y']['start']
        self.yf = cuboid_json['y']['end']
    
    def copy(self):
        return Cuboid(self.tojson())

    def tojson(self):
        cuboid_json = {}
        cuboid_json['id'] = self.id
        cuboid_json['x'] = {'start': self.rect.get('xi'), 'end': self.rect.get('xf')}
        cuboid_json['z'] = {'start': self.rect.get('zi'), 'end': self.rect.get('zf')}
        cuboid_json['y'] = {'start': self.yi, 'end': self.yf}
        return cuboid_json
        
    def is_subset(self, cuboid_2):
        in_y = self.yi >= cuboid_2.yi and self.yf <= cuboid_2.yf
        in_rect = self.rect.is_subset(cuboid_2.rect)
        return in_y and in_rect
        
    def volume(self):
        return (self.yf - self.yi) * self.rect.area()

    def __str__(self):
        out_string = str(self.rect)
        out_string += '\nyi: ' + str(self.yi) + '  yf: ' + str(self.yf)
        
        return out_string

    
        
