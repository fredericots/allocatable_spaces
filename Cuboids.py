import json
import collections

from Cuboid import Cuboid

class Cuboids:
    
    def __init__(self, cuboid_list = []):
        self.cuboids = [cuboid.copy() for cuboid in cuboid_list]
        self._icuboid = 0
        self.cuboidsid = 0
    
    def read(self, cuboids_file):
        f = open(cuboids_file, 'r')
        cuboids_list = json.load(f)
        self.cuboids = [Cuboid(jcuboid) for jcuboid in cuboids_list]
    
    def add(self, yi, yf, rect):
        cuboid_json = {}
        cuboid_json['x'] = {'start': rect.get('xi'), 'end': rect.get('xf')}
        cuboid_json['z'] = {'start': rect.get('zi'), 'end': rect.get('zf')}
        cuboid_json['y'] = {'start': yi, 'end': yf}
        cuboid_json['id'] = self.cuboidsid
        self.cuboidsid += 1
        self.cuboids.append(Cuboid(cuboid_json))
    
    def tojson(self):
        cuboids_json = [cuboid.tojson() for cuboid in self.cuboids]
        return cuboids_json
    
    def get_all_yi(self):
        return [cuboid.yi for cuboid in self.cuboids]
        
    def get_all_yf(self):
        return [cuboid.yf for cuboid in self.cuboids]
    
    def yi_counter(self):
        all_yi = self.get_all_yi()
        return collections.Counter(all_yi)

    def yi_mergeables(self):
        yi_mergeables = []
        counter = self.yi_counter()
        for yi in counter:
            if counter[yi] > 1:
                yi_mergeables.append(yi)
        return yi_mergeables

    def avg_volume(self):
        volume = 0
        for cuboid in self.cuboids:
            volume += cuboid.volume()
        return volume / len(self.cuboids)
    
    def cuboid_max_volume(self):
        max_volume = 0
        max_index = 0
        cuboid_max = None
        for i in range(len(self.cuboids)):
            cuboid = self.cuboids[i]
            vol = cuboid.volume()
            if vol > max_volume:
                cuboid_max = cuboid.copy()
                max_index = i
                max_volume = vol
        return cuboid_max, max_index
            
    def reset_id(self):
        for i in range(len(self.cuboids)):
            self.cuboids[i].id = i
    
    
#### functions with 'all' returns a cuboids object
    def all_withyi(self, yi):
        return self.all_withyi_list([yi])

    def all_withyi_list(self, yi_list):
        withyi_list = []
        for cuboid in self.cuboids:
            if cuboid.yi in yi_list:
                withyi_list.append(cuboid)
        return Cuboids(withyi_list)

    def all_not_mergeables(self):
        not_merge_list = []
        counter = self.yi_counter()
        for yi in counter:
            if counter[yi] == 1:
                for cubo in self.cuboids:
                    if cubo.yi == yi:
                        not_merge_list.append(cubo)
        return Cuboids(not_merge_list)
        
    def rectangles_with_ylimits(self, yi, yf):
        y_limits = []
        for cuboid in self.cuboids:
            if cuboid.yi <= yi and cuboid.yf >= yf:
                y_limits.append(cuboid.rect.copy())
        return y_limits

    def rectangles_withyf(self, yf, mode):
        rect_all = []
        for cuboid in self.cuboids:
            if mode == 'lesser' and cuboid.yf <= yf:
                rect_all.append(cuboid.rect.copy())
            elif mode == 'greater' and cuboid.yf >= yf:
                rect_all.append(cuboid.rect.copy())
            elif mode == 'equal' and cuboid.yf == yf:
                rect_all.append(cuboid.rect.copy())
        
        return rect_all
    
#### ITERABLE FUNCTIONS
    def __iter__(self):
        return self
    
    def __next__(self):
        if self._icuboid == len(self.cuboids):
            raise StopIteration
        
        cuboid = self.cuboids[self._icuboid]
        self._icuboid += 1
        return cuboid.copy()
        
    def __len__(self):
        return len(self.cuboids)
    
    def __getitem__(self, i):
        return self.cuboids[i]
    
    def __str__(self):
        out_string = str(self.rect)
        out_string += '\nyi: ' + str(self.yi) + '  yf: ' + str(self.yf)
        
        return out_string



    
    
