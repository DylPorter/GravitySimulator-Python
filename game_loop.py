import pyray, logic, math, textbox

class Window:
    def __init__(self):
        self.window_width = logic.window_width
        self.window_height = logic.window_height
        pyray.set_target_fps(1000)

    def start(self):
        pyray.init_window(self.window_width, self.window_height, "Hello")

        menu = pyray.Rectangle(10, 10, 300, 300)

        menu_string_1 = "radius"
        menu_box_1 = textbox.Box(pyray.Vector2(menu.x+20, menu.y+60), pyray.Vector2(menu.width-50, 50), 2)

        body_initialised = False

        while not pyray.window_should_close():
            print(len(logic.bodies))
            mouse_pos = pyray.get_mouse_position()

            if pyray.is_key_down(32):
                timestep = 0
            else:
                timestep = pyray.get_frame_time()

            if pyray.is_mouse_button_pressed(0):
                menu_box_1.click(mouse_pos)

                if pyray.check_collision_point_rec(mouse_pos, menu) == False:
                    radius = menu_box_1.get_value()

                    if radius == 0:
                        radius = 10

                    new_body = logic.Body(pyray.get_mouse_position(),   # Position
                                          pyray.vector2_zero(),         # Velocity
                                          radius)

                    logic.bodies.append(new_body)
                    body_initialised = True

            if pyray.is_mouse_button_released(0) and body_initialised == True:

                dist = new_body.find_x_y_distance(mouse_pos)

                if new_body.is_outside_circle(dist, new_body.get_rad()) == True:
                    new_body.push_velocity(dist)

                new_body.make_active()
                body_initialised = False

            for body in logic.bodies:
                body_position = body.get_pos()
                
                if (-self.window_width*1.2 < body_position.x < self.window_width*1.2) == False or \
                        (-self.window_height*1.2 < body_position.y < self.window_height*1.2) == False:
                    logic.bodies.remove(body)
                    continue

                if body.check_active() == True:
                    body.update_position(timestep)

                    for other in logic.bodies:
                        if body != other and other.check_active() == True:
                            body.calculate_vel_acc(other, timestep)

                            if body.collision_check(other) == True:
                                body.calculate_collision_velocity(other)

                                if body.get_rad() > 2: 
                                    mass_ratio = body.get_mass() / other.get_mass()
                                    print(mass_ratio)

                                    if mass_ratio <= 0.9:
                                        body_children = body.collapse(other)
                                        
                                        for child in body_children:
                                            logic.bodies.append(child)

                                        if len(body_children) > 0:
                                            logic.bodies.remove(body)
                                            break

                                    elif 0.9 < mass_ratio <= 1.1:
                                        body_children = body.collapse(other)
                                        other_children = other.collapse(body)
                                        
                                        for child in body_children:
                                            logic.bodies.append(child)
                                        for child in other_children:
                                            logic.bodies.append(child)

                                        if len(body_children) > 0:
                                            logic.bodies.remove(body)
                                            if len(other_children) > 0:
                                                logic.bodies.remove(other)
                                            break
                                        elif len(other_children) > 0:
                                            logic.bodies.remove(other)
                                            if len(body_children) > 0:
                                                logic.bodies.remove(body)
                                            break

                                    else:
                                        other_children = other.collapse(body)
                                        
                                        for child in other_children:
                                            logic.bodies.append(child)

                                        if len(other_children) > 0:
                                            logic.bodies.remove(other)
                                            break
                                else:
#                                    print(body.get_rad(), other.get_rad())
                                    other.increase_size(1)
#                                    print(other.get_rad(), "updated")
                                    logic.bodies.remove(body)
                                    break

            pyray.begin_drawing()
            pyray.clear_background(pyray.BLACK)

            for i in logic.bodies:
                if i.check_active() == False:
                    pyray.draw_line_v(i.get_pos(), pyray.get_mouse_position(), pyray.YELLOW)

                pyray.draw_circle_v(i.get_pos(), i.get_rad(), i.get_colour())

            pyray.draw_rectangle_rec(menu, pyray.GRAY)
            pyray.draw_text(menu_string_1, 30, 30, 30, pyray.BLACK)

            menu_box_1.draw()

            pyray.end_mode_2d()
            pyray.end_drawing()


window = Window()
window.start()
