import pyray, logic

def save():
    data_2d_array = []

    for body in logic.bodies:
        body_data = []
        if body.get_active() == True:
            body_data.append(body.get_density())
            body_data.append(body.get_pos())
            body_data.append(body.get_vel())
            body_data.append(body.get_acc())
            body_data.append(body.get_rad())
            body_data.append(body.get_momentum())
            
            data_2d_array.append(body_data)

    file = open("save_game.txt", "w")

    for item in data_2d_array:
        file.write("%s/%s/%s/%s/%s/%s/%s/%s/%s/%s\n" % (item[0],                # Density
                                                        item[1].x, item[1].y,   # Position
                                                        item[2].x, item[2].y,   # Velocity
                                                        item[3].x, item[3].y,   # Acceleration
                                                        item[4],                # Radius
                                                        item[5].x, item[5].y))  # Momentum
    
    file.close()


def load():
    try:
        file = open("save_game.txt", "r")
        data = file.readlines()
        file.close()
    except:
        data = []
    
    for line in data:
        body_info = []
        value = ""

        for char in line:
            if char == "/" or char == "\n":
                print("a")
                body_info.append(value)
                value = ""
                continue
            value += char

        if int(body_info[0]) == 1:
            new_body = logic.Planet(pyray.Vector2(float(body_info[1]), float(body_info[2])),
                                    pyray.Vector2(float(body_info[3]), float(body_info[4])),
                                    pyray.Vector2(float(body_info[5]), float(body_info[6])),
                                    int(body_info[7]),
                                    pyray.Vector2(float(body_info[8]), float(body_info[9])),
                                    True)
        elif int(body_info[0]) == 10:
            new_body = logic.Star(pyray.Vector2(float(body_info[1]), float(body_info[2])),
                                  pyray.Vector2(float(body_info[3]), float(body_info[4])),
                                  pyray.Vector2(float(body_info[5]), float(body_info[6])),
                                  int(body_info[7]),
                                  pyray.Vector2(float(body_info[8]), float(body_info[9])),
                                  True)
        else:
            new_body = logic.Hole(pyray.Vector2(float(body_info[1]), float(body_info[2])),
                                  pyray.Vector2(float(body_info[3]), float(body_info[4])),
                                  pyray.Vector2(float(body_info[5]), float(body_info[6])),
                                  int(body_info[7]),
                                  pyray.Vector2(float(body_info[8]), float(body_info[9])),
                                  True)


        logic.bodies.append(new_body)
    
    

    
