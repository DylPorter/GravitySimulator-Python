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

        menu = pyray.Rectangle(10, 10, 200, 270)
        sort_box = pyray.Rectangle(self.win_width-140, 10, 130, 370)

        menu_string_1 = "radius (max: 99)"
        menu_box_1 = ui.Box(pyray.Vector2(menu.x+20, menu.y+50), 
                            pyray.Vector2(menu.width-40, 30), 2)
        menu_string_2 = "rankings"
        
        pause_menu = ui.PopUp()
        tooltip = ui.PopUp()
        tooltip_rec = None

        button_1 = ui.Button(pyray.Vector2(menu.x+20, menu.y+100), 
                             pyray.Vector2(menu.width-40, 30), "Planet", True)
        button_2 = ui.Button(pyray.Vector2(menu.x+20, menu.y+140), 
                             pyray.Vector2(menu.width-40, 30), "Star", True)
        button_3 = ui.Button(pyray.Vector2(menu.x+20, menu.y+180), 
                             pyray.Vector2(menu.width-40, 30), "Black Hole", True)
        button_4 = ui.Button(pyray.Vector2(menu.x+20, menu.y+220),
                             pyray.Vector2(menu.width-40, 30), "Repel Gravity", True)
        button_5 = ui.Button(pyray.Vector2(pyray.get_screen_width()/2 - 290, 
                                           pyray.get_screen_height() - 70),
                             pyray.Vector2(170, 50), "Reset", False)
        button_6 = ui.Button(pyray.Vector2(pyray.get_screen_width()/2 + 120, 
                                           pyray.get_screen_height() - 70),
                             pyray.Vector2(170, 50), "Quit", False)

        button_array = [button_1, button_2, button_3]
        button_1.switch_on()

        body_initialised = False
        body_moving = False

        while running: 
            if pyray.is_key_pressed(256) or pyray.window_should_close():
                if pause_menu.get_active():
                    pause_menu.make_inactive()
                    button_5.show_off()
                    button_6.show_off()
                else:
                    pause_menu.make_active("pause_menu")
                    button_5.show_on()
                    button_6.show_on()
                    #file_access.save()
                    #running = False

            if button_5.get_active():
                button_5.switch_off()
                logic.bodies = []
                pause_menu.make_inactive()
                button_5.show_off()
                button_6.show_off()

            if button_6.get_active():
                button_6.switch_off()
                file_access.save()
                running = False

            mouse_pos = pyray.get_mouse_position()

            if pyray.is_key_down(32) or pause_menu.get_active():
                timestep = 0
            else:
                timestep = pyray.get_frame_time()

            menu_string_3 = ""
            menu_string_4 = ""

            ranking_length = len(logic.bodies)
            if len(logic.bodies) > 10:
                ranking_length = 10

            for i in range(ranking_length):
                menu_string_3 += f"{i+1}.\n\n"
                menu_string_4 += f"{logic.bodies[i].get_rad()}\n\n"

            if pyray.is_mouse_button_pressed(0):
                menu_box_1.click(mouse_pos)
                button_1.click(mouse_pos, button_array)
                button_2.click(mouse_pos, button_array)
                button_3.click(mouse_pos, button_array)
                button_4.click(mouse_pos)
                button_5.click(mouse_pos)
                button_6.click(mouse_pos)

                tooltip.box_click(mouse_pos)

                if button_4.get_active():
                    logic.repulsion = -1
                else:
                    logic.repulsion = 1

                if not pyray.check_collision_point_rec(mouse_pos, menu) and \
                        not pyray.check_collision_point_rec(mouse_pos, sort_box) and \
                        not pause_menu.get_active():

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
                                radius = 1

                            body_type = None

                            if button_1.get_active():
                                new_body = logic.Planet(mouse_pos,              # Position
                                                        pyray.vector2_zero(),   # Velocity
                                                        pyray.vector2_zero(),   # Acceleration
                                                        radius,                 # Radius
                                                        pyray.vector2_zero(),   # Momentum
                                                        False)                  # is_active
                            elif button_2.get_active():
                                new_body = logic.Star(mouse_pos,                # Position
                                                      pyray.vector2_zero(),     # Velocity
                                                      pyray.vector2_zero(),     # Acceleration
                                                      radius,                   # Radius
                                                      pyray.vector2_zero(),     # Momentum
                                                      False)                    # is_active
                            elif button_3.get_active():
                                new_body = logic.Hole(mouse_pos,                # Position
                                                      pyray.vector2_zero(),     # Velocity
                                                      pyray.vector2_zero(),     # Acceleration
                                                      radius,                   # Radius
                                                      pyray.vector2_zero(),     # Momentum
                                                      False)                    # is_active

                            logic.bodies.append(new_body)
                            body_initialised = True

            if pyray.is_mouse_button_released(0) and body_initialised:

                dist = new_body.find_x_y_distance(mouse_pos)

                if new_body.is_outside_circle(dist):
                    new_body.push_velocity(pyray.Vector2(dist.x*2, dist.y*2))

                new_body.make_active()
                body_initialised = False

                logic.bodies = logic.selection_sort(logic.bodies)
                
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

                    logic.bodies = logic.selection_sort(logic.bodies)

            pyray.begin_drawing()
            pyray.clear_background(pyray.BLACK)

            for i in logic.bodies:
                if not i.get_active():
                    pyray.draw_line_v(i.get_pos(), pyray.get_mouse_position(), pyray.YELLOW)

                pyray.draw_circle_v(i.get_pos(), i.get_rad(), i.get_colour())

            pyray.draw_rectangle_rec(menu, pyray.LIGHTGRAY)
            pyray.draw_text(menu_string_1, 30, 30, 20, pyray.BLACK)

            pyray.draw_rectangle_rec(sort_box, pyray.LIGHTGRAY)
            pyray.draw_text(menu_string_2, self.win_width-120, 30, 20, pyray.BLACK)
            pyray.draw_text(menu_string_3, self.win_width-120, 70, 20, pyray.BLACK)
            pyray.draw_text(menu_string_4, self.win_width-90, 70, 20, pyray.BLACK)

            pause_menu.draw()
            menu_box_1.draw()
            button_1.draw()
            button_2.draw()
            button_3.draw()
            button_4.draw()
            button_5.draw()
            button_6.draw()

            tooltip.draw()

            pyray.end_mode_2d()
            pyray.end_drawing()

        pyray.close_window()


window = Window()
window.start()
