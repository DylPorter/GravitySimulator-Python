import pyray

class Box:
    def __init__(self, pos, size, char_limit):
        self.__pos = pos
        self.__size = size
        self.__char_limit = char_limit
        self.__is_active = False
        
        self.__text = ""

        self.__rec = pyray.Rectangle(self.__pos.x, self.__pos.y, self.__size.x, self.__size.y)

    def click(self, mouse_pos):
        if pyray.check_collision_point_rec(mouse_pos, self.__rec):
            self.__is_active = True
        else:
            self.__is_active = False
        
    def draw(self):
        pyray.draw_rectangle_rec(self.__rec, pyray.WHITE)

        pyray.draw_text(str(self.__text), int(self.__pos.x+5), int(self.__pos.y+5), 40, pyray.BLACK)

        if self.__is_active:
            pyray.draw_rectangle_lines_ex(self.__rec, 2, pyray.RED)

            character = pyray.get_char_pressed()
            while character > 0:
                if 48 <= character <= 57 and len(self.__text) < self.__char_limit:
                    self.__text += chr(character)
                character = pyray.get_char_pressed()
            if pyray.is_key_pressed(259) and len(self.__text) > 0:
                self.__text = self.__text[:-1]
                
    def get_value(self):
        x = 0
        if self.__text != "":
            x = int(self.__text)

        return x

