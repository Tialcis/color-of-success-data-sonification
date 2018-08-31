# this is a foreshadowing of the next stage,
# where we will make classes that are the heart of object-oriented programming
# but for now we won't take advantage of the power of OOP--
# as we will only have one "instance" of each kind of animation.
# The next NB will use entirely OOP.

# this is a little class that lets the "patches" object not stretch the dots...
# it won't make any sense for now, but later it hopefully will !
# i found it somewhere but forgot to record where !
# but i think there is a probably a simpler way to do this now !
# maybe by rescaling the data to [0,1] and then writing the axis labels as the real values ?

class GraphDist() :
    def __init__(self, size, ax, x=True) :
        self.size = size
        self.ax = ax
        self.x = x

    @property
    def dist_real(self) :
        x0, y0 = self.ax.transAxes.transform((0, 0)) # lower left in pixels
        x1, y1 = self.ax.transAxes.transform((1, 1)) # upper right in pixes
        value = x1 - x0 if self.x else y1 - y0
        return value

    @property
    def dist_abs(self) :
        bounds = self.ax.get_xlim() if self.x else self.ax.get_ylim()
        return bounds[0] - bounds[1]

    @property
    def value(self) :
        return (self.size / self.dist_real) * self.dist_abs

    def __mul__(self, obj) :
        return self.value * obj
