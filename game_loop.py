import pyray, logic

class Window:
    def __init__(self):
        self.window_width = 1800
        self.window_height = 1450
        pyray.set_target_fps(60)

    def start(self):
        pyray.init_window(self.window_width, self.window_height, "Hello")

        while not pyray.window_should_close():
            if pyray.is_key_down(32):
                timestep = 0
            else:
                timestep = pyray.get_frame_time()


            print(timestep)
            if pyray.is_mouse_button_pressed(0):
                new_body = logic.Body(pyray.get_mouse_position(),   # Position
                                      pyray.vector2_zero(),         # Velocity
                                      pyray.vector2_zero(),         # Acceleration
                                      15,                           # Radius
                                      pyray.WHITE)                  # Colour
                logic.bodies.append(new_body)

            for body in logic.bodies:
                for other in logic.bodies:
                    if body != other:
                        body.update_position(timestep)
                        body.calculate_vel_acc(other, timestep)

            pyray.begin_drawing()
            pyray.clear_background(pyray.BLACK)

            for i in logic.bodies:
                pyray.draw_circle_v(i.pos, i.radius, i.colour)

            pyray.end_mode_2d()

            pyray.end_drawing()

window = Window()
window.start()
