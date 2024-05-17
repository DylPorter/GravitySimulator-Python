import pyray, logic

class Window:
    def __init__(self):
        self.window_width = 800
        self.window_height = 450
        pyray.set_target_fps(60)

    def start(self):
        pyray.init_window(self.window_width, self.window_height, "Hello")

        while not pyray.window_should_close():
            timestep = pyray.get_frame_time()

            if pyray.is_mouse_button_pressed(0):
                new_planet = logic.Planet(pyray.get_mouse_position(),   # Position
                                          15,                           # Radius
                                          pyray.WHITE,                  # Colour
                                          pyray.vector2_zero(),         # Velocity
                                          pyray.vector2_zero())         # Acceleration
                logic.bodies.append(new_planet)


            pyray.begin_drawing()
            pyray.clear_background(pyray.BLACK)

            for i in logic.bodies:
                pyray.draw_circle_v(i.pos, i.radius, i.colour)

            pyray.end_mode_2d()

            pyray.end_drawing()

window = Window()
window.start()
