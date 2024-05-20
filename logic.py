import pyray, math

class Body:
    def __init__(self, pos, v, a, radius, colour):
        self.prev_pos = pos
        self.pos = pos
        self.v = v
        self.a = a
        self.radius = radius
        self.colour = colour

        # Consider adding self.density, value between 0 to 1 to multiply the mass by

        self.mass = math.pi * ((self.radius)**2) # Area of a circle

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


bodies = []
