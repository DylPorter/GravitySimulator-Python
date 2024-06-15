import pyray, logic

def save():
    data_2d_array = []

    for body in logic.bodies:
        body_data = []
        if body.get_active() == True:
            body_data.append(body.get_pos())
            body_data.append(body.get_vel())
            body_data.append(body.get_acc())
            body_data.append(body.get_rad())
            body_data.append(body.get_momentum())
            
            data_2d_array.append(body_data)

    file = open("save_game.txt", "w")

    for item in data_2d_array:
        file.write("%s/%s/%s/%s/%s/%s/%s/%s/%s\n" % (item[0].x, item[0].y,      # Position
                                                     item[1].x, item[1].y,      # Velocity
                                                     item[2].x, item[2].y,      # Acceleration
                                                     item[3],                   # Radius
                                                     item[4].x, item[4].y))     # Momentum
    
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

        new_body = logic.Body(pyray.Vector2(float(body_info[0]), float(body_info[1])),
                              pyray.Vector2(float(body_info[2]), float(body_info[3])),
                              pyray.Vector2(float(body_info[4]), float(body_info[5])),
                              int(body_info[6]),
                              pyray.Vector2(float(body_info[7]), float(body_info[8])),
                              True)

        logic.bodies.append(new_body)
    
    

    
