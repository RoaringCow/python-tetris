import time
import keyboard
import threading
import os
class Block:
    def __init__(self, shape):
        # 0  1  2  3
        # 4  5  6  7
        # 8  9 10 11        You input the places that are the block like [1,5,9,13] which is a stick
        # 12 13 14 15
        self.x_coordinate = 0
        self.y_coordinate = 0
        self.shape_list = shape
        self.canMove = True
        big_star_list = []
        for x in self.shape_list:
            star_list = []
            star_x, star_y = x % 4, int(x / 4)
            star_list.append(star_x)
            star_list.append(star_y)
            big_star_list.append(star_list)
        self.start_coordinate = big_star_list  # I know it is a bad name
        print(self.start_coordinate)

    def spawn(self, arena):
        self.x_coordinate = int(len(arena[0]) / 2) - 1
        for i in self.start_coordinate:
            x_pos = i[0] + self.x_coordinate
            y_pos = i[1] + self.y_coordinate
            arena[y_pos][x_pos] = "*"

    def can_fall(self, arena):
        for i in self.start_coordinate:
            x_pos = i[0] + self.x_coordinate
            y_pos = i[1] + self.y_coordinate
            if arena[y_pos + 1][x_pos] == "n":
                return False
            elif arena[y_pos + 1][x_pos] == "*":
                temp_list = []
                for x in self.start_coordinate:
                    temp_list.append([(x[0] + self.x_coordinate), x[1] + self.y_coordinate])
                if [x_pos, y_pos + 1] not in temp_list:
                    return False

                elif arena[y_pos + 1][x_pos] == "n":
                    return False
        return True

    def can_move_right(self, arena):
        for i in self.start_coordinate:
            x_pos = i[0] + self.x_coordinate
            y_pos = i[1] + self.y_coordinate
            if arena[y_pos][x_pos + 1] == "|":
                return False
            if arena[y_pos][x_pos + 1] == "*":
                # a list to make the codes below shorter
                added_list = []
                for j in self.start_coordinate:
                    # soldaki bir koordinatın diğerleri ile aynı olup olmadığını kontrol
                    added_list.append([j[0] + self.x_coordinate, j[1] + self.y_coordinate])
                if [x_pos + 1, y_pos] not in added_list:
                    return False
        return True

    def can_move_left(self, arena):
        for i in self.start_coordinate:
            x_pos = i[0] + self.x_coordinate
            y_pos = i[1] + self.y_coordinate
            if arena[y_pos][x_pos - 1] == "|":
                return False
            if arena[y_pos][x_pos - 1] == "*":
                # a list to make the codes below shorter
                added_list = []
                for j in self.start_coordinate:
                    # soldaki bir koordinatın diğerleri ile aynı olup olmadığını kontrol
                    added_list.append([j[0] + self.x_coordinate, j[1] + self.y_coordinate])
                if [x_pos - 1, y_pos] not in added_list:
                    return False
        return True

    def clear_old_pos(self, arena):
        for i in self.start_coordinate:
            x_pos = i[0] + self.x_coordinate
            y_pos = i[1] + self.y_coordinate
            arena[y_pos][x_pos] = " "

    def fall(self, arena):
        for i in self.start_coordinate:
            x_pos = i[0] + self.x_coordinate
            y_pos = i[1] + self.y_coordinate + 1
            arena[y_pos][x_pos] = "*"
        self.y_coordinate += 1

    def move_left(self, arena):
        for i in self.start_coordinate:
            x_pos = i[0] + self.x_coordinate - 1
            y_pos = i[1] + self.y_coordinate
            arena[y_pos][x_pos] = "*"
        self.x_coordinate -= 1

    def move_right(self, arena):
        for i in self.start_coordinate:
            x_pos = i[0] + self.x_coordinate + 1
            y_pos = i[1] + self.y_coordinate
            arena[y_pos][x_pos] = "*"
        self.x_coordinate += 1

    def check_arena(self, arena):
        mark_pos = []
        check_list = ["*"] * (len(arena[0]) - 1)
        check_list.append("|")
        for index, x in enumerate(arena):
            if x == check_list:
                mark_pos.append(index)
        return mark_pos

    def destroy_line(self, arena, mark_pos):
        for x in range(len(arena) - 2, -1, -1):  # -2 to skip the floor
            number_of_lines_to_fall = 0  # hahahaha bad name :(
            for y in mark_pos:
                if y > x:
                    number_of_lines_to_fall += 1
            arena[x + number_of_lines_to_fall] = arena[x]
            arena[x] = [" "] * (len(arena[0]) - 1)
            arena[x].append("|")


def print_arena():
    for x in arena:
        string = ""
        for y in x:
            string += y
        print(string)

# form the area
arena = []
width_list = []
width = 10     # int(input("Width?:  "))
height = 10    # int(input("height?:  "))
for x in range(height):
    for y in range(width):
        width_list.append(" ")
    width_list.append("|")
    arena.append(width_list)
    width_list = []
arena.append(list("n" for x in range(width + 1)))

# shape_list = [[0, 4, 8, 12], [0, 1, 2 , 3], ]

# shape1 = Block([0, 1, 2, 3])
shape1 = Block([0, 4, 8, 12])
shape1.spawn(arena)

def fall_thread():
    while True:
        os.system("cls")
        print_arena()
        if shape1.can_fall(arena):
            shape1.clear_old_pos(arena)
            shape1.fall(arena)
            os.system("cls")
            print_arena()
        else:
            if shape1.canMove:
                shape1.canMove = False
            else:
                line_check = shape1.check_arena(arena)
                if line_check: # eğer boş değilse
                    shape1.destroy_line(arena, line_check)
                shape1.y_coordinate = 0
                shape1.spawn(arena)

        time.sleep(0.6)


def move_thread():
    while True:
        if keyboard.is_pressed("a"):
            if shape1.can_move_left(arena):
                shape1.clear_old_pos(arena)
                shape1.move_left(arena)
                os.system("cls")
                print_arena()
        elif keyboard.is_pressed("d"):
            if shape1.can_move_right(arena):
                shape1.clear_old_pos(arena)
                shape1.move_right(arena)
                os.system("cls")
                print_arena()
        time.sleep(0.2)

t1 = threading.Thread(target=fall_thread)
t2 = threading.Thread(target=move_thread)
t1.start()
t2.start()
