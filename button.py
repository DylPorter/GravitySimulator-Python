import pyray

class Button:
    def __init__(self, pos, size, text):
        self.__pos = pos
        self.__size = size
        self.__text = text

        self.__shape = ""
        self.__clicked = False

        self.__rec = pyray.Rectangle(self.__pos.x, self.__pos.y, self.__size.x, self.__size.y)

    def hover(self, mouse_pos):
        if pyray.check_collision_point_rec(mouse_pos, self.__rec):
            self.__clicked = True

    def draw(self):
        pyray.draw_rectangle_rec(self.__rec, pyray.DARKGRAY)
        pyray.draw_text(str(self.__text), int(self.__pos.x+5), int(self.__pos.y+5), 30, pyray.BLACK)

    def switch(self):
        if self.__clicked == True:
            self.__clicked = False
        else:
            self.__clicked = True

