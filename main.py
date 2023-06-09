from tkinter import *
# окно на закрытие окна игры
from tkinter import messagebox
import time
import random

# создаем объект
tk = Tk()

# переменная которая определять запущению окно игры или нет
app_running = True

# def tesxr():
#     s = int(input('Введите размер поля: '))
#     return s
# q = tesxr()

# размеры окна
size_canvas_x = 500
size_canvas_y = 500
s_x = s_y = 8  # размер игрового поля
s_y = 8  # размер игрового поля
# размер шагов между ячейками
step_x = size_canvas_x // s_x  # шаг по горизонтали
step_y = size_canvas_y // s_y  # шаг по вертикали
# переопределим ширину и высоту окна игры чтобы не было зазоров по бокам
size_canvas_x = step_x * s_x
size_canvas_y = step_y * s_y
# добавим к игровому полю еще пространство, что бы не нарушалось целостность игрового поля
# и также меню равно 4 ячейкам поля
menu_x = step_x * 4  # 250
menu_y = 40
# максимально количество кораблей для игрового поля
# ships = s_x // 2
ships = 5
# длина первого типа корабля
ships_len1 = s_x // 5
# длина второго типа корабля
ships_len2 = s_x // 3
# длина третьего типа корабля
ships_len3 = s_x // 2
# генерация кораблей противника
enemy_ships1 = [[0 for i in range(s_x + 1)] for i in range(s_y + 1)]
# генерация кораблей игрока
enemy_ships2 = [[0 for i in range(s_x + 1)] for i in range(s_y + 1)]
# print(enemy_ships1)
# список объектов  canvas
list_ids = []

# points1 список куда мы кликнули мышкой
points1 = [[-1 for i in range(s_x)] for i in range(s_y)]
points2 = [[-1 for i in range(s_x)] for i in range(s_y)]
# boom - список попаданий по кораблям противника
boom = [[0 for i in range(s_x)] for i in range(s_y)]

# ships_list - список кораблей игрока1 и игрока2
ships_list = []

def on_closing():
    # объявляем переменную глобальной чтобы она не принимала новое значение в функции
    global app_running
    # если происходит закрытие окна
    if messagebox.askokcancel('Выход из игры', 'Хотите выйти из игры?'):
        app_running = False
        # уничтожение объекта при закрытии
        tk.destroy()


# закрытие окна
tk.protocol('WM_DELETE_WINDOW', on_closing)

# параметры окна
tk.title('Игра морской бой')
# запрет на изменения окна игры
tk.resizable(0, 0)
# окно игры поверх всех окон
tk.wm_attributes("-topmost", 1)
# окно игры с нашими параметрами которые мы задавали раньше
canvas = Canvas(tk, width=size_canvas_x + menu_x + size_canvas_x, height=size_canvas_y + menu_y, bd=0,
                highlightthickness=0)
# создаем окно в виде прямоугольника заливка(fill)
canvas.create_rectangle(0, 0, size_canvas_x, size_canvas_y, fill='white')
canvas.create_rectangle(size_canvas_x + menu_x, 0, size_canvas_x + menu_x + size_canvas_x, size_canvas_y,
                        fill="lightyellow")
# упаковка нашего окна
canvas.pack()
# обновление нашего объекта
tk.update()


# функция, которая рисует поля игры
def draw_table(offset_x=0):  # offset_x=0 - не обязательный элемент
    for i in range(0, s_x + 1):
        canvas.create_line(offset_x + step_x * i, 0, offset_x + step_x * i, size_canvas_y)
    for i in range(0, s_x + 1):
        canvas.create_line(offset_x, step_y * i, offset_x + size_canvas_x, step_y * i)


draw_table()
# вызываем второй раз функцию для создания игрового поля
draw_table(size_canvas_x + menu_x)

# добавляем информацию в нижнее поля где прописано игрок1 и игрок2
t0 = Label(tk, text="Игрок №1", font=("Helvetica", 16))
# центровка надписи игрок1
t0.place(x=size_canvas_x // 2 - t0.winfo_reqwidth() // 2, y=size_canvas_y + 3)
t1 = Label(tk, text="Игрок №2", font=("Helvetica", 16))
# центровка надписи игрок2
t1.place(x=size_canvas_x + menu_x + size_canvas_x // 2 - t1.winfo_reqwidth() // 2, y=size_canvas_y + 3)

# пометить какой игрок ходит
t0.configure(bg='red')
t0.configure(bg='#f0f0f0')


def button_show_enemy1():
    for i in range(0, s_x):
        for j in range(0, s_y):
            if enemy_ships1[j][i] > 0:
                color = 'red'
                if points1[j][i] != -1:
                    color = 'green'
                _id = canvas.create_rectangle(i * step_x, j * step_y, i * step_x + step_x, j * step_y + step_y,
                                              fill=color)
                list_ids.append(_id)


def button_show_enemy2():
    for i in range(0, s_x):
        for j in range(0, s_y):
            if enemy_ships2[j][i] > 0:
                color = 'red'
                if points2[j][i] != -1:
                    color = 'green'
                _id = canvas.create_rectangle(size_canvas_x + menu_x + i * step_x, j * step_y, size_canvas_x + menu_x + i * step_x + step_x, j * step_y + step_y,
                                              fill=color)
                list_ids.append(_id)


def button_begin_again():
    global list_ids
    global points1, points2
    global boom
    global enemy_ships1, enemy_ships2

    for el in list_ids:
        canvas.delete(el)
    list_ids = []
    generate_ships_list()
    print(ships_list)
    enemy_ships1 = generate_enemy_ships()
    enemy_ships2 = generate_enemy_ships()
    points1 = [[-1 for i in range(s_x)] for i in range(s_y)]
    points2 = [[-1 for i in range(s_x)] for i in range(s_y)]
    boom = [[0 for i in range(s_x)] for i in range(s_y)]


# добавляем кнопки
b0 = Button(tk, text='Показать корабли Игрока №1', command=button_show_enemy1)
# добавляем кнопки на панель и смещаем их чтобы они небыли на игровом поле
b0.place(x=size_canvas_x + 20, y=30)


b1 = Button(tk, text='Показать корабли Игрока №2', command=button_show_enemy2)
# добавляем кнопки на панель и смещаем их чтобы они небыли на игровом поле
b1.place(x=size_canvas_x + 20, y=70)


# добавляем кнопки на панель и смещаем их чтобы они небыли на игровом поле
b2 = Button(tk, text="Начать заново!", command=button_begin_again)
b2.place(x=size_canvas_x + 20, y=110)


# отрисовка кружочка и крестика на игровом поле
def draw_point(x, y):
    # print(enemy_ships1[y][x])
    if enemy_ships1[y][x] == 0:
        color = 'red'
        id1 = canvas.create_oval(x * step_x, y * step_y, x * step_x + step_x, y * step_y + step_y, fill=color)
        id2 = canvas.create_oval(x * step_x + step_x // 3, y * step_y + step_y // 3, x * step_x + step_x - step_x // 3,
                                 y * step_y + step_y - step_y // 3, fill="white")
        list_ids.append(id1)
        list_ids.append(id2)
    if enemy_ships1[y][x] > 0:
        color = 'blue'
        id1 = canvas.create_rectangle(x * step_x, y * step_y + step_y // 2 - step_y // 10, x * step_x + step_x,
                                      y * step_y + step_y // 2 + step_y // 10, fill=color)
        id2 = canvas.create_rectangle(x * step_x + step_x // 2 - step_x // 10, y * step_y,
                                      x * step_x + step_x // 2 + step_x // 10, y * step_y + step_y, fill=color)
        list_ids.append(id1)
        list_ids.append(id2)


def check_winner(x, y):
    win = False
    if enemy_ships1[y][x] > 0:
        boom[y][x] = enemy_ships1[y][x]
    sum_enemy_ships1 = sum(sum(i) for i in zip(*enemy_ships1))
    sum_boom = sum(sum(i) for i in zip(*boom))
    print(f'Сумм: {sum_enemy_ships1}, {sum_boom}')
    if sum_enemy_ships1 == sum_boom:
        win = True
    return win


def check_winner2():
    win = True
    for i in range(0, s_x):
        for j in range(0, s_y):
            if enemy_ships1[j][i] > 0:
                if points1[j][i] == -1:
                    win = False
    print(win)
    return win


def add_to_all(event):
    global points1
    _type = 0  # левая кнопка мыши
    if event.num == 3:
        _type = 1  # правая кнопка мыши
    # print(_type)
    # координаты при нажатии на кнопки
    mouse_x = canvas.winfo_pointerx() - canvas.winfo_rootx()
    mouse_y = canvas.winfo_pointery() - canvas.winfo_rooty()
    # print(mouse_x, mouse_y)
    # получаем координаты ячейки на игровом поле
    ip_x = mouse_x // step_x
    ip_y = mouse_y // step_y
    # print(ip_x, ip_y, '_type', _type)
    # ip_x ip_y - это игровое поле проверка, что бы мы не выходили за рамки игривого поля
    if ip_x < s_x and ip_y < s_y:
        if points1[ip_y][ip_x] == -1:
            points1[ip_y][ip_x] = _type
            draw_point(ip_x, ip_y)
            # if check_winner(ip_x, ip_y):
            if check_winner2():
                print('Победа')
                points1 = [[10 for i in range(s_x)] for i in range(s_y)]
        # print(len(list_ids))


canvas.bind_all('<Button-1>', add_to_all)  # левая кнопка мыши
canvas.bind_all('<Button-3>', add_to_all)  # правая кнопка мыши


def generate_ships_list():
    global ships_list
    ships_list = []
    # генерация кораблей по размерам
    for i in range(0, ships):
        ships_list.append(random.choice([ships_len1, ships_len2, ships_len3]))






def generate_enemy_ships():
    global ships_list
    enemy_ships = []

    # print(ships_list)
    # подсчет суммарной длинны коробля
    sum_1_all_ships = sum(ships_list)
    sum_1_enemy = 0

    while sum_1_enemy != sum_1_all_ships:
        # обнуляем массив кораблей врага
        enemy_ships = [[0 for i in range(s_x + 1)] for i in
                        range(s_y + 1)]  # +1 для доп. линии справа и снизу, для успешных проверок генерации противника

        for i in range(0, ships):
            len = ships_list[i]
            horizont_vertikal = random.randrange(1, 3)  # 1- горизонтальное 2 - вертикальное

            primerno_x = random.randrange(0, s_x)
            if primerno_x + len > s_x:
                primerno_x = primerno_x - len

            primerno_y = random.randrange(0, s_y)
            if primerno_y + len > s_y:
                primerno_y = primerno_y - len

            # print(horizont_vertikal, primerno_x,primerno_y)
            if horizont_vertikal == 1:
                if primerno_x + len <= s_x:
                    for j in range(0, len):
                        try:
                            check_near_ships = 0
                            check_near_ships = enemy_ships[primerno_y][primerno_x - 1] + \
                                               enemy_ships[primerno_y][primerno_x + j] + \
                                               enemy_ships[primerno_y][primerno_x + j + 1] + \
                                               enemy_ships[primerno_y + 1][primerno_x + j + 1] + \
                                               enemy_ships[primerno_y - 1][primerno_x + j + 1] + \
                                               enemy_ships[primerno_y + 1][primerno_x + j] + \
                                               enemy_ships[primerno_y - 1][primerno_x + j]
                            # print(check_near_ships)
                            if check_near_ships == 0:  # записываем в том случае, если нет ничего рядом
                                enemy_ships[primerno_y][primerno_x + j] = i + 1  # записываем номер корабля
                        except Exception:
                            pass
            if horizont_vertikal == 2:
                if primerno_y + len <= s_y:
                    for j in range(0, len):
                        try:
                            check_near_ships = 0
                            check_near_ships = enemy_ships[primerno_y - 1][primerno_x] + \
                                               enemy_ships[primerno_y + j][primerno_x] + \
                                               enemy_ships[primerno_y + j + 1][primerno_x] + \
                                               enemy_ships[primerno_y + j + 1][primerno_x + 1] + \
                                               enemy_ships[primerno_y + j + 1][primerno_x - 1] + \
                                               enemy_ships[primerno_y + j][primerno_x + 1] + \
                                               enemy_ships[primerno_y + j][primerno_x - 1]
                            # print(check_near_ships)
                            if check_near_ships == 0:  # записываем в том случае, если нет ничего рядом
                                enemy_ships[primerno_y + j][primerno_x] = i + 1  # записываем номер корабля
                        except Exception:
                            pass

        # делаем подсчет 1ц
        sum_1_enemy = 0
        for i in range(0, s_x):
            for j in range(0, s_y):
                if enemy_ships[j][i] > 0:
                    sum_1_enemy = sum_1_enemy + 1

        # print(sum_1_enemy)
        # print(ships_list)
        # print(enemy_ships)
    return enemy_ships


generate_ships_list()
print(ships_list)
enemy_ships1 = generate_enemy_ships()
enemy_ships2 = generate_enemy_ships()
# print('******************')
# print(enemy_ships1)
# print('******************')
# print(enemy_ships2)


# цикл для работы нашего приложения
while app_running:
    if app_running:
        # обновление нашего окна
        tk.update_idletasks()
        tk.update()
    time.sleep(0.005)
