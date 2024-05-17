import pyray
from logic import Logic

class Window:
    def __init__(self):
        self.logic = Logic()

        pyray.init_window(800, 450, "Hello")
        pyray.set_target_fps(60)

    def start(self):
        while not pyray.window_should_close():

            if pyray.is_mouse_button_down(0):
                self.logic.positions.append(pyray.get_mouse_position())

            pyray.begin_drawing()
            pyray.clear_background(pyray.BLACK)

            for i in self.logic.positions:
                pyray.draw_circle_v(i, 20, pyray.WHITE)

            pyray.end_mode_2d()

            pyray.end_drawing()

window = Window()
window.start()
