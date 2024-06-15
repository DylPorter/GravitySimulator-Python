import pyray, logic, math, ui, file_access

class Window:
    def __init__(self):
        self.win_width = logic.window_width
        self.win_height = logic.window_height
        pyray.set_target_fps(1000)

        file_access.load()

    def start(self):
        pyray.init_window(self.win_width, self.win_height, "Hello")
        running = True

        menu = pyray.Rectangle(10, 10, 200, 230)

        menu_string_1 = "radius (max: 99)"
        menu_box_1 = ui.Box(pyray.Vector2(menu.x+20, menu.y+50), 
                            pyray.Vector2(menu.width-40, 30), 2)
        
        pause_menu = ui.PopUp()
        tooltip = ui.PopUp()
        tooltip_rec = None

        button_1 = ui.Button(pyray.Vector2(menu.x+20, menu.y+100), 
                             pyray.Vector2(menu.width-40, 30), "Planet")
        button_2 = ui.Button(pyray.Vector2(menu.x+20, menu.y+140), 
                             pyray.Vector2(menu.width-40, 30), "Star")
        button_3 = ui.Button(pyray.Vector2(menu.x+20, menu.y+180), 
                             pyray.Vector2(menu.width-40, 30), "Black Hole")
        button_array = [button_1, button_2, button_3]
        button_1.switch_on()

        body_initialised = False
        body_moving = False

        while running: 
            if pyray.is_key_pressed(256) or pyray.window_should_close():
                file_access.save()
                running = False

            mouse_pos = pyray.get_mouse_position()

            if pyray.is_key_down(32):
                timestep = 0
            else:
                timestep = pyray.get_frame_time()

            if pyray.is_mouse_button_pressed(0):
                menu_box_1.click(mouse_pos)
                button_1.click(mouse_pos, button_array)
                button_2.click(mouse_pos, button_array)
                button_3.click(mouse_pos, button_array)

                tooltip.box_click(mouse_pos)

                if not pyray.check_collision_point_rec(mouse_pos, menu):

                    if tooltip.get_active():
                        if not pyray.check_collision_point_rec(mouse_pos, tooltip_rec):
                            tooltip.make_inactive()
                    else:
                        for body in logic.bodies:
                            if not body.is_outside_circle(body.find_x_y_distance(mouse_pos)):
                                tooltip.make_active("tooltip", body)
                                tooltip_rec = tooltip.return_rec()
                                break
                        else:
                            radius = menu_box_1.get_value()

                            if radius == 0:
                                radius = 10

                            new_body = logic.Body(pyray.get_mouse_position(),   # Position
                                                  pyray.vector2_zero(),         # Velocity
                                                  pyray.vector2_zero(),         # Acceleration
                                                  radius,                       # Radius
                                                  pyray.vector2_zero(),         # Momentum
                                                  False)                        # is_active

                            logic.bodies.append(new_body)
                            body_initialised = True

            if pyray.is_mouse_button_released(0) and body_initialised:

                dist = new_body.find_x_y_distance(mouse_pos)

                if new_body.is_outside_circle(dist):
                    new_body.push_velocity(pyray.Vector2(dist.x*2, dist.y*2))

                new_body.make_active()
                body_initialised = False
                
            if pyray.is_mouse_button_pressed(1):
                for focus_body in logic.bodies:
                    if not focus_body.is_outside_circle(focus_body.find_x_y_distance(mouse_pos)):
                        focus_body.make_inactive()
                        body_moving = True
                        break

            if pyray.is_mouse_button_down(1) and body_moving:
                focus_body.set_new_position(mouse_pos)

            if pyray.is_mouse_button_released(1) and body_moving: 
                focus_body.make_active() 
                body_moving = False


            for body in logic.bodies:
                body_position = body.get_pos()
                
                if not (-self.win_width*1.2 < body_position.x < self.win_width*1.2) or \
                        not (-self.win_height*1.2 < body_position.y < self.win_height*1.2):
                    logic.bodies.remove(body)
                    continue

                if len(logic.bodies) > 100:
                    if body.get_rad() <= 2:
                        logic.bodies.remove(body)
                        continue

                if body.check_active():
                    body.update_position(timestep)

                    for other in logic.bodies:
                        if body != other and other.check_active():
                            body.calculate_vel_acc(other, timestep)

                            if body.collision_check(other):
                                body.calculate_collision_velocity(other)

                                if body.get_rad() > 2: 
                                    mass_ratio = body.get_mass() / other.get_mass()

                                    if mass_ratio <= 0.8:
                                        body_children = body.collapse(other)
                                        
                                        for child in body_children:
                                            logic.bodies.append(child)

                                        if len(body_children) > 0:
                                            logic.bodies.remove(body)
                                            break

                                    elif 0.8 < mass_ratio <= 1.2:
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
                                    other.increase_size(1)
                                    logic.bodies.remove(body)
                                    break

            pyray.begin_drawing()
            pyray.clear_background(pyray.BLACK)

            for i in logic.bodies:
                if i.get_colour() == pyray.RED:
                    pyray.draw_line_v(i.get_pos(), pyray.get_mouse_position(), pyray.YELLOW)

                pyray.draw_circle_v(i.get_pos(), i.get_rad(), i.get_colour())

            pyray.draw_rectangle_rec(menu, pyray.LIGHTGRAY)
            pyray.draw_text(menu_string_1, 30, 30, 20, pyray.BLACK)

            menu_box_1.draw()
            button_1.draw()
            button_2.draw()
            button_3.draw()

            pause_menu.draw()
            tooltip.draw()

            pyray.end_mode_2d()
            pyray.end_drawing()

        pyray.close_window()


window = Window()
window.start()
