import pyray, math

class Planet:
    def __init__(self, pos, radius, colour, v, a):
        self.pos = pos
        self.radius = radius
        self.colour = colour
        self.v = v
        self.a = a

        # Consider adding self.density, value between 0 to 1 to multiply the mass by

        self.mass = math.pi * ((self.radius)**2) # Area of a circle

    def update_position(self, timestep):
        pass
    
    def calculate_velocity(self, other, timestep):
        pass

    def calculate_acceleration(self, other):
        force = self.find_force(other)

        self.a.x = force.x / self.mass
        self.a.y = force.y / self.mass

    def find_force(self, other):    # Newton's Law of Universal Gravitation
        G = 6.674                   # G ~= 6.674 * 10^-11

        x_dist = (other.pos.x - self.pos.x)
        y_dist = (other.pos.y - self.pos.y)
        
        x_force = (G * (self.mass * other.mass)) / math.pow(x_dist, 2)
        y_force = (G * (self.mass * other.mass)) / math.pow(y_dist, 2)

        return pyray.Vector2(x_force, y_force)


bodies = []
