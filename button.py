import pyray

class Button:
    def __init__(self, pos, size, text):
        self.__pos = pos
        self.__size = size
        self.__text = text

        self.__shape = ""
        self.__clicked = False

        self.__rec = pyray.Rectangle(self.__pos.x, self.__pos.y, self.__size.x, self.__size.y)

    def click(self, mouse_pos, button_array):
        if pyray.check_collision_point_rec(mouse_pos, self.__rec):
            self.switch_on()

            for other in button_array:
                if self == other:
                    continue
                if other.get_active() == True:
                    other.switch_off()

    def draw(self):
        pyray.draw_rectangle_rec(self.__rec, pyray.GRAY)
        pyray.draw_text(str(self.__text), int(self.__pos.x+5), int(self.__pos.y+5), 20, pyray.BLACK)
        
        if self.__clicked == True:
            pyray.draw_rectangle_lines_ex(self.__rec, 2, pyray.RED)
        else:
            pyray.draw_rectangle_lines_ex(self.__rec, 2, pyray.GRAY)

    def switch_on(self):
        self.__clicked = True

    def switch_off(self):
        self.__clicked = False

    def get_active(self):
        return self.__clicked

