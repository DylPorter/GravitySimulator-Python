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

        pyray.draw_text(str(self.__text), int(self.__pos.x+5), int(self.__pos.y+5), 20, pyray.BLACK)

        if self.__is_active:
            pyray.draw_rectangle_lines_ex(self.__rec, 2, pyray.RED)

            character = pyray.get_char_pressed()
            while character > 0:
                if 48 <= character <= 57 and len(self.__text) < self.__char_limit:
                    self.__text += chr(character)
                character = pyray.get_char_pressed()
            if pyray.is_key_pressed(259) and len(self.__text) > 0:
                self.__text = self.__text[:-1]
        else:
            pyray.draw_rectangle_lines_ex(self.__rec, 2, pyray.GRAY)
                
    def get_value(self):
        x = 10
        if self.__text != "":
            x = int(self.__text)

        return x

    def get_active(self):
        return self.__is_active

    def set_text(self, value):
        self.__text = value


class Button:
    def __init__(self, pos, size, text, show):
        self.__pos = pos
        self.__size = size
        self.__text = text
        self.__show = show

        self.__shape = ""
        self.__clicked = False

        if self.__text == "Reset" or self.__text == "Quit":
            self.__font_size = 30
        else:
            self.__font_size = 20

        self.__rec = pyray.Rectangle(self.__pos.x, self.__pos.y, self.__size.x, self.__size.y)

    def click(self, mouse_pos, button_array = None):
        if pyray.check_collision_point_rec(mouse_pos, self.__rec):
            if button_array == None:
                if not self.__clicked:
                    self.switch_on()
                else:
                    self.switch_off()
            else:
                self.switch_on()

            try:
                for other in button_array:
                    if self == other:
                        continue
                    if other.get_active():
                        other.switch_off()
            except:
                pass

    def draw(self):
        if self.__show:
            pyray.draw_rectangle_rec(self.__rec, pyray.GRAY)
            pyray.draw_text(str(self.__text), int(self.__pos.x+5), int(self.__pos.y+5), self.__font_size, pyray.BLACK)
            
            if self.__clicked:
                pyray.draw_rectangle_lines_ex(self.__rec, 2, pyray.RED)
            else:
                pyray.draw_rectangle_lines_ex(self.__rec, 2, pyray.GRAY)

    def switch_on(self):
        self.__clicked = True

    def switch_off(self):
        self.__clicked = False

    def show_on(self):
        self.__show = True

    def show_off(self):
        self.__show = False

    def get_active(self):
        return self.__clicked


class PopUp:
    def __init__(self):
        self.__pos = pyray.vector2_zero()
        self.__size = pyray.vector2_zero()
        self.__is_active = False
        self.__object = None
        self.__child_box = None


    def draw(self):
        if self.__is_active:
            pyray.draw_rectangle_v(self.__pos, self.__size, pyray.LIGHTGRAY)

            # Pause Menu
            if self.__child_box == None:
                pyray.draw_text("PAUSED", int(self.__pos.x)+240, int(self.__pos.y)+20, 30, pyray.BLACK)                
                
            # Tooltip
            else:
                pyray.draw_text("radius", int(self.__pos.x)+10, int(self.__pos.y)+10, 20, pyray.BLACK)
                if not self.__child_box.get_active():
                    self.__child_box.set_text(str(self.__object.get_rad()))
                self.__child_box.draw()

            

    def get_active(self):
        return self.__is_active

    def make_active(self, popup_type, clicked_object=None):
        self.__is_active = True
        self.__object = clicked_object

        if self.__object != None:
            self.__object.change_colour(pyray.BLUE)

        if popup_type == "tooltip":
            self.__size.x = 100
            self.__size.y = 80
            self.__pos = pyray.get_mouse_position()

            self.__child_box = Box(pyray.Vector2(self.__pos.x+10, self.__pos.y+40),
                                   pyray.Vector2(self.__size.x-20, 30), 2)

        elif popup_type == "pause_menu":
            self.__size.x = 600
            self.__size.y = 70
            self.__pos.x = pyray.get_screen_width()/2 - 300
            self.__pos.y = pyray.get_screen_height() - 80

    def make_inactive(self):
        self.__is_active = False
        if self.__object != None:
            self.__object.change_colour(self.__object.get_set_colour())

    def box_click(self, point):
        if self.__is_active:
            self.__child_box.click(point)
            if not self.__child_box.get_active():
                new_rad = self.__child_box.get_value()
                if new_rad < 1:
                    new_rad = 1
                self.__object.set_new_radius(new_rad)

    def return_rec(self):
        return pyray.Rectangle(self.__pos.x, self.__pos.y, self.__size.x, self.__size.y)
