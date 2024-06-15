import pyray, math, random

window_width = 1200
window_height = 1200

bodies = []

class Body:
    def __init__(self, pos, v, a, radius, momentum, is_active):
        self.__pos = pos
        self.__v = v
        self.__a = a
        self.__radius = radius
        self.__momentum = momentum
        self.__is_active = is_active

        self.__mass = math.pow(self.__radius, 2)

        if is_active:
            self.__colour = pyray.WHITE
        else:
            self.__colour = pyray.RED


    def update_position(self, timestep):
        self.__mass = math.pow(self.__radius, 2)
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

        self.__momentum.x = self.__mass * self.__v.x
        self.__momentum.y = self.__mass * self.__v.y

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

    
    def set_new_position(self, vector):
        self.__pos = vector


    def set_new_velocity(self, vector):
        self.__v = vector


    def set_new_radius(self, radius):
        self.__radius = radius


    def find_x_y_distance(self, point):
        x_dist = (point.x - self.__pos.x)
        y_dist = (point.y - self.__pos.y)

        return pyray.Vector2(x_dist, y_dist)
    

    def is_outside_circle(self, dist):
        return ((math.pow(dist.x, 2) + math.pow(dist.y, 2)) > math.pow(self.__radius, 2))


    def make_active(self):
        self.__is_active = True
        self.__colour = pyray.WHITE


    def make_inactive(self):
        self.__is_active = False

    
    def collision_check(self, other):
        if pyray.check_collision_circles(self.__pos, self.__radius, 
                                         other.get_pos(), other.get_rad()):
            return True


    def collapse(self, other):
        children = []
        num_children = 10

        if self.__radius < 10:
            num_children = math.ceil(self.__radius)
        
        for i in range(num_children):
            child = Body(pyray.Vector2(self.__pos.x + self.__radius * random.uniform(-1, 1),
                                       self.__pos.y + self.__radius * random.uniform(-1, 1)),
                         pyray.Vector2(self.__v.x * 0.2,
                                       self.__v.y * 0.2),
                         pyray.vector2_zero(),
                         math.ceil(self.__radius / num_children),
                         pyray.vector2_zero(),
                         True)

            random_vec = pyray.Vector2(int(self.__v.x * random.random()),
                                       int(self.__v.y * random.random()))
            child.push_velocity(random_vec)
            children.append(child)

        return children


    def calculate_collision_velocity(self, other):
        other_mass = other.get_mass()
        other_v = other.get_vel()

        normal_vec = self.find_x_y_distance(other.get_pos())
        hypo = math.sqrt(math.pow(normal_vec.x, 2) + math.pow(normal_vec.y, 2))

        # unit normal & tangent vectors of the 2 circles
        u_norm_vec = pyray.Vector2((normal_vec.x / hypo), (normal_vec.y / hypo))
        u_tan_vec = pyray.Vector2(-u_norm_vec.y, u_norm_vec.x) 

        # project velocity onto the vectors with dot product to get scalar 1-dimensional values
        self_normal_vel = (u_norm_vec.x * self.__v.x) + (u_norm_vec.y * self.__v.y)
        self_tangent_vel = (u_tan_vec.x * self.__v.x) + (u_tan_vec.y * self.__v.y)

        other_normal_vel = (u_norm_vec.x * other_v.x) + (u_norm_vec.y * other_v.y)
        other_tangent_vel = (u_tan_vec.x * other_v.x) + (u_tan_vec.y * other_v.y)

        # calculate scalar values of new normal velocities
        self_new_vel = (self_normal_vel * (self.__mass - other_mass) +
                (2 * other_mass * other_normal_vel)) / (self.__mass + other_mass)
        other_new_vel = (other_normal_vel * (other_mass - self.__mass) +
                (2 * self.__mass * self_normal_vel)) / (self.__mass + other_mass)

        # convert scalar values back into vector values
        self_new_vel_vec = pyray.Vector2((self_new_vel * u_norm_vec.x) + 
                                         (self_tangent_vel * u_tan_vec.x),
                                         (self_new_vel * u_norm_vec.y) +
                                         (self_tangent_vel * u_tan_vec.y))

        other_new_vel_vec = pyray.Vector2((other_new_vel * u_norm_vec.x) + 
                                          (other_tangent_vel * u_tan_vec.x),
                                          (other_new_vel * u_norm_vec.y) +
                                          (other_tangent_vel * u_tan_vec.y))

        self.set_new_velocity(self_new_vel_vec)
        other.set_new_velocity(other_new_vel_vec)


    def change_colour(self, colour):
        self.__colour = colour
    
    def increase_size(self, amount):
        if self.__radius < 99:
            self.__radius += amount

    def check_active(self):
        return self.__is_active

    def get_pos(self):
        return self.__pos
    
    def get_vel(self):
        return self.__v

    def get_rad(self):
        return self.__radius

    def get_acc(self):
        return self.__a

    def get_momentum(self):
        return self.__momentum

    def get_active(self):
        return self.__is_active
    
    def get_mass(self):
        return self.__mass

    def get_colour(self):
        return self.__colour
