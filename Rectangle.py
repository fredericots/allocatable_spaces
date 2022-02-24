import matplotlib.pyplot as plt
import matplotlib.patches as patches

from Segment import Segment, group_all_segments

class Rectangle:

    def __init__(self, xi, xf, zi, zf):
        self.segx = Segment(xi, xf)
        self.segz = Segment(zi, zf)
        
        self.linewidth = 2
        self.edgecolor = 'k'
        self.facecolor = 'none'
        
    def patch(self):
        xi = self.segx.xi
        xf = self.segx.xf
        zi = self.segz.xi
        zf = self.segz.xf
        x_size = xf - xi
        z_size = zf - zi
        rect = patches.Rectangle((xi, zi),
                                 x_size, z_size,
                                 linewidth = self.linewidth, 
                                 edgecolor = self.edgecolor, 
                                 facecolor = self.facecolor)
        return rect
    
    def is_subset(self, rectangle_2):
        in_x = self.segx.is_subset(rectangle_2.segx)
        in_z = self.segz.is_subset(rectangle_2.segz)
        return in_x and in_z
    
    def area(self):
        dx = self.segx.xf - self.segx.xi
        dz = self.segz.xf - self.segz.xi
        return dx * dz
    
    def intersects(self, rectangle_2, side = None):
        xint = self.segx.intersects(rectangle_2.segx)
        zint = self.segz.intersects(rectangle_2.segz)
        if side == 'xi':
            xint = xint and (rectangle_2.segx.xi < self.segx.xi)
        elif side == 'xf':
            xint = xint and (rectangle_2.segx.xf > self.segx.xf)
        elif side == 'zi':
            zint = zint and (rectangle_2.segz.xi < self.segz.xi)
        elif side == 'zf':
            zint = zint and (rectangle_2.segz.xf > self.segz.xf)
        
        return xint and zint

    def find_intersects(self, rect_list, direction):
        dir_intersects = []
        for rect in rect_list:
            if self.intersects(rect, direction):
                dir_intersects.append(rect)
        return dir_intersects
    
    def get(self, var):
        if var == 'segx':
            return self.segx
        elif var == 'segz':
            return self.segz
        elif var == 'xi':
            return self.segx.xi
        elif var == 'xf':
            return self.segx.xf
        elif var == 'zi':
            return self.segz.xi
        elif var == 'zf':
            return self.segz.xf

    def set_value(self, var, value):
        if var == 'segx':
            self.segx = value
        elif var == 'segz':
            self.segz = value
        elif var == 'xi':
            self.segx.xi = value
        elif var == 'xf':
            self.segx.xf = value
        elif var == 'zi':
            self.segz.xi = value
        elif var == 'zf':
            self.segz.xf = value
    
    def copy(self):
        xi = self.segx.xi
        xf = self.segx.xf
        zi = self.segz.xi
        zf = self.segz.xf
        return Rectangle(xi, xf, zi, zf)
        
    def __str__(self):
        return 'Segx: ' + str(self.segx) + ' Segz: ' + str(self.segz)

    
def plot_rectangles(all_rectangles, x_range = [0,100], y_range = [0,100]):

    fig, ax = plt.subplots()
    ax.set_xlim(x_range[0], x_range[1])
    ax.set_ylim(y_range[0], y_range[1])
    
    for rect in all_rectangles:
        rect_patch = rect.patch()
        ax.add_patch(rect_patch)
    
    plt.show()    

    