import pyray, math

window_width = 1000
window_height = 1000

class Body:
    def __init__(self, pos, v, a, radius, colour):
        self.pos = pos
        self.v = v
        self.a = a
        self.radius = radius
        self.colour = colour

        # Consider adding self.density, value between 0 to 1 to multiply the mass by

        self.mass = math.pi * math.pow(self.radius, 2) # Area of a circle

    def update_position(self, timestep):
        self.pos.x += (self.v.x * timestep) + (0.5 * self.a.x * math.pow(timestep, 2))
        self.pos.y += (self.v.y * timestep) + (0.5 * self.a.y * math.pow(timestep, 2))
        # x(t+dt) = x(t) + v(t)dt + (1/2)(a)(t^2)
        
    def calculate_vel_acc(self, other, timestep):
        force = self.find_force(other)

        new_a_x = force.x / self.mass      # F = m * a (rearrange)
        new_a_y = force.y / self.mass      # a = F / m

        self.v.x += 0.5 * (self.a.x + new_a_x) * timestep     # v(t+dt) = v(t) + (1/2)at
        self.v.y += 0.5 * (self.a.y + new_a_y) * timestep

        self.a.x = new_a_x
        self.a.y = new_a_y

    def find_force(self, other):    # Newton's Law of Universal Gravitation
        G = 66.74                   # G ~= 6.674 * 10^-11

        x_dist = (other.pos.x - self.pos.x) # Solve for the triangle
        y_dist = (other.pos.y - self.pos.y)
        hypo = math.sqrt(math.pow(x_dist, 2) + math.pow(y_dist, 2))
        
        force = G * (self.mass * other.mass) / math.pow(hypo, 2) # Newton's formula
        
        x_force = force * (x_dist / hypo) # Convert to unit vector for the direction
        y_force = force * (y_dist / hypo)

        return pyray.Vector2(x_force, y_force)
    
    def is_in_boundary(corner, width, height):
        if corner.x < self.pos.x < (corner.x + width) and corner.y < self.pos.y < (corner.y + height):
            return True


class Node:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.body = None
        self.centre = pyray.vector2_zero()
        self.total_mass = 0
        self.body_count = 0

        self.leaf = True
        self.children = []

    def split(self):
        half_width = 0.5 * self.width
        half_height = 0.5 * self.height

        self.children.append(Node(x, y, half_width, half_height)) # nw
        self.children.append(Node(x+half_width, y, half_width, half_height)) # ne
        self.children.append(Node(x, y+half_height, half_width, half_height)) # sw
        self.children.append(Node(x+half_width, y+half_height, half_width, half_height)) # se

    def add_body(self, new_body):
        if self.leaf == True:
            if self.body == None:
                pass
            self.centre.x += new_body.pos.x # Find a better way to add the centre of mass
            self.centre.y += new_body.pos.y
            self.total_mass += new_body.mass
            self.body_count += 1
        pass

bodies = []
