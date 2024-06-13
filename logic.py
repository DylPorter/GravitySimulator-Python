import pyray, math, random

window_width = 1000
window_height = 1000

bodies = []

class Body:
    def __init__(self, pos, v, a, radius, mass):
        self.__pos = pos
        self.__v = v
        self.__a = a
        self.__radius = radius
        self.__mass = mass 

        self.__colour = pyray.RED
        self.__is_active = False


    def update_position(self, timestep):
#        self.__radius = math.sqrt(self.__mass/3)
        self.__pos.x += (self.__v.x * timestep) + (0.5 * self.__a.x * math.pow(timestep, 2))
        self.__pos.y += (self.__v.y * timestep) + (0.5 * self.__a.y * math.pow(timestep, 2))
        # x(t+dt) = x(t) + v(t)dt + (1/2)(a)(t^2)

        
    # BUG: objects speed up the more objects there are... why???
    def calculate_vel_acc(self, other, timestep):
        force = self.find_force(other)

        new_a_x = force.x / self.__mass      # F = m * a (rearrange)
        new_a_y = force.y / self.__mass      # a = F / m

        self.__v.x += 0.5 * (self.__a.x + new_a_x) * timestep     # v(t+dt) = v(t) + (1/2)at
        self.__v.y += 0.5 * (self.__a.y + new_a_y) * timestep

        self.__a.x = new_a_x
        self.__a.y = new_a_y


    def find_force(self, other):    # Newton's Law of Universal Gravitation
        G = 667.4                   # G ~= 6.674 * 10^-11

        distances = self.find_x_y_distance(other.get_pos())
        hypo = math.sqrt(math.pow(distances.x, 2) + math.pow(distances.y, 2))

        force = G * (self.__mass * other.get_mass()) / math.pow(hypo, 2) # Newton's formula

        # Convert to unit vector for the direction
        x_force = force * (distances.x / hypo)
        y_force = force * (distances.y / hypo)

        return pyray.Vector2(x_force, y_force)


    def push_position(self, value_vec):
        self.__pos.x += value_vec.x
        self.__pos.y += value_vec.y


    def push_velocity(self, value_vec):
        self.__v.x += value_vec.x
        self.__v.y += value_vec.y


    def find_x_y_distance(self, point):
        x_dist = (point.x - self.__pos.x)
        y_dist = (point.y - self.__pos.y)

        return pyray.Vector2(x_dist, y_dist)
    

    def is_outside_circle(self, dist, radius):
        return ((math.pow(dist.x, 2) + math.pow(dist.y, 2)) > math.pow(radius, 2))


    def make_active(self):
        self.__is_active = True
        self.__colour = pyray.WHITE

    
    def collision_check(self, other):
        if pyray.check_collision_circles(self.__pos, self.__radius, other.get_pos(), other.get_rad()):
            return True


    def collapse(self, other):
        children = []
        
        for i in range(10):
            child = Body(pyray.Vector2(self.__pos.x + random.random(),
                                       self.__pos.y + random.random()),
                         pyray.vector2_zero(),
                         pyray.vector2_zero(),
                         math.ceil(self.__radius/10),
                         math.ceil(self.__mass/10))

            random_vec = pyray.Vector2(int(self.__v.x * 0.01 * random.random()),
                                       int(self.__v.y * 0.01 * random.random()))

            child.push_velocity(random_vec)
            child.make_active()

            children.append(child)

        return children

    
    def increase_mass(self, amount):
        self.__mass += amount

    def check_active(self):
        return self.__is_active

    def get_pos(self):
        return self.__pos

    def get_rad(self):
        return self.__radius
    
    def get_colour(self):
        return self.__colour

    def get_mass(self):
        return self.__mass

