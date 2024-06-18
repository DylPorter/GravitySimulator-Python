import pyray, math, random

window_width = 1200
window_height = 1200
repulsion = 1

bodies = []

class Planet:
    def __init__(self, pos, v, a, radius, momentum, is_active):
        self._pos = pos
        self._v = v
        self._a = a
        self._radius = radius
        self._momentum = momentum
        self._is_active = is_active
        self._density = 1

        self._mass = math.pow(self._radius, 2)
        self._set_colour = pyray.WHITE

        if not is_active:
            self._colour = pyray.RED
        else:
            self._colour = self._set_colour


    def update_position(self, timestep):
        self._mass = math.pow(self._radius, 2) * self._density
        self._pos.x += (self._v.x * timestep) + (0.5 * self._a.x * math.pow(timestep, 2))
        self._pos.y += (self._v.y * timestep) + (0.5 * self._a.y * math.pow(timestep, 2))
        # x(t+dt) = x(t) + v(t)dt + (1/2)(a)(t^2)

        
    # BUG: objects speed up the more objects there are... why???
    def calculate_vel_acc(self, other, timestep):
        force = self.find_force(other)

        new_a_x = force.x / self._mass      # F = m * a (rearrange)
        new_a_y = force.y / self._mass      # a = F / m
         
        # v(t+dt) = v(t) + (1/2)at
        self._v.x += 0.5 * (self._a.x + new_a_x) * timestep * repulsion
        self._v.y += 0.5 * (self._a.y + new_a_y) * timestep * repulsion

        self._momentum.x = self._mass * self._v.x
        self._momentum.y = self._mass * self._v.y

        self._a.x = new_a_x
        self._a.y = new_a_y


    def find_force(self, other):    # Newton's Law of Universal Gravitation
        G = 667.4                   # G ~= 6.674 * 10^-11

        distances = self.find_x_y_distance(other.get_pos())
        hypo = math.sqrt(math.pow(distances.x, 2) + math.pow(distances.y, 2))

        force = G * (self._mass * other.get_mass()) / math.pow(hypo, 2) # Newton's formula

        # Convert to unit vector for the direction
        x_force = force * (distances.x / hypo)
        y_force = force * (distances.y / hypo)

        return pyray.Vector2(x_force, y_force)


    def push_position(self, value_vec):
        self._pos.x += value_vec.x
        self._pos.y += value_vec.y


    def push_velocity(self, value_vec):
        self._v.x += value_vec.x
        self._v.y += value_vec.y

    
    def set_new_position(self, vector):
        self._pos = vector


    def set_new_velocity(self, vector):
        self._v = vector


    def set_new_radius(self, radius):
        self._radius = radius


    def find_x_y_distance(self, point):
        x_dist = (point.x - self._pos.x)
        y_dist = (point.y - self._pos.y)

        return pyray.Vector2(x_dist, y_dist)
    

    def is_outside_circle(self, dist):
        return ((math.pow(dist.x, 2) + math.pow(dist.y, 2)) > math.pow(self._radius, 2))


    def make_active(self):
        self._is_active = True
        self.change_colour(self._set_colour)

    def make_inactive(self):
        self._is_active = False

    
    def collision_check(self, other):
        if pyray.check_collision_circles(self._pos, self._radius, 
                                         other.get_pos(), other.get_rad()):
            return True


    def collapse(self, other):
        children = []
        num_children = 10

        if self._radius < 10:
            num_children = math.ceil(self._radius)
        
        for i in range(num_children):
            child = Planet(pyray.Vector2(self._pos.x + self._radius * random.uniform(-1, 1),
                                         self._pos.y + self._radius * random.uniform(-1, 1)),
                           pyray.Vector2(self._v.x * 0.2,
                                         self._v.y * 0.2),
                           pyray.vector2_zero(),
                           math.ceil(self._radius / num_children),
                           pyray.vector2_zero(),
                           True)

            random_vec = pyray.Vector2(int(self._v.x * random.random()),
                                       int(self._v.y * random.random()))
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
        self_normal_vel = (u_norm_vec.x * self._v.x) + (u_norm_vec.y * self._v.y)
        self_tangent_vel = (u_tan_vec.x * self._v.x) + (u_tan_vec.y * self._v.y)

        other_normal_vel = (u_norm_vec.x * other_v.x) + (u_norm_vec.y * other_v.y)
        other_tangent_vel = (u_tan_vec.x * other_v.x) + (u_tan_vec.y * other_v.y)

        # calculate scalar values of new normal velocities
        self_new_vel = (self_normal_vel * (self._mass - other_mass) +
                (2 * other_mass * other_normal_vel)) / (self._mass + other_mass)
        other_new_vel = (other_normal_vel * (other_mass - self._mass) +
                (2 * self._mass * self_normal_vel)) / (self._mass + other_mass)

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
        self._colour = colour
    
    def increase_size(self, amount):
        if self._radius < 99:
            self._radius += amount

    def check_active(self):
        return self._is_active

    def get_pos(self):
        return self._pos
    
    def get_vel(self):
        return self._v

    def get_rad(self):
        return self._radius

    def get_acc(self):
        return self._a

    def get_momentum(self):
        return self._momentum

    def get_active(self):
        return self._is_active
    
    def get_mass(self):
        return self._mass

    def get_colour(self):
        return self._colour

    def get_set_colour(self):
        return self._set_colour

    def get_density(self):
        return self._density


class Star(Planet):
    def __init__(self, pos, v, a, radius, momentum, is_active):
        super().__init__(pos, v, a, radius, momentum, is_active)

        self._density = 10
        self._set_colour = pyray.YELLOW

        if not is_active:
            self._colour = pyray.RED
        else:
            self._colour = self._set_colour


class Hole(Planet):
    def __init__(self, pos, v, a, radius, momentum, is_active):
        super().__init__(pos, v, a, radius, momentum, is_active)

        self._density = 100
        self._set_colour = pyray.DARKGRAY

        if not is_active:
            self._colour = pyray.RED
        else:
            self._colour = self._set_colour
    
    
def selection_sort(body_array):
    for i in range(len(body_array)):
        max_body_index = i

        for j in range(i+1, len(body_array)):
            if body_array[max_body_index].get_rad() < body_array[j].get_rad():
                max_body_index = j

        (body_array[max_body_index], body_array[i]) = (body_array[i], body_array[max_body_index])

    return body_array

