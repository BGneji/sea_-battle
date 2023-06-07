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
size_canvas_x = 600
size_canvas_y = 600
s_x = s_y = 5  # размер игрового поля
s_y = 5 # размер игрового поля
# размер шагов между ячейками
step_x = size_canvas_x // s_x  # шаг по горизонтали
step_y = size_canvas_y // s_y  # шаг по вертикали
# переопределим ширину и высоту окна игры чтобы не было зазоров по бокам
size_canvas_x = step_x * s_x
size_canvas_y = step_y * s_y
# добавим к игровому полю еще пространство, что бы не нарушалось целостность игрового поля
menu_x = 250
# максимально количество кораблей для игрового поля
ships = s_x // 2
# длина первого типа корабля
ships_len1 = s_x // 5
# длина второго типа корабля
ships_len2 = s_x // 3
# длина третьего типа корабля
ships_len3 = s_x // 2

enemy_ships = [[0 for i in range(s_x + 1)] for i in range(s_y + 1)]
# print(enemy_ships)
# список объектов  canvas
list_ids = []


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
canvas = Canvas(tk, width=size_canvas_x + menu_x, height=size_canvas_y, bd=0, highlightthickness=0)
# создаем окно в виде прямоугольника заливка(fill)
canvas.create_rectangle(0, 0, size_canvas_x, size_canvas_y, fill='white')
# упаковка нашего окна
canvas.pack()
# обновление нашего объекта
tk.update()


# функция, которая рисует поля игры
def draw_table():
    for i in range(0, s_x + 1):
        canvas.create_line(step_x * i, 0, step_x * i, size_canvas_y)
    for i in range(0, s_x + 1):
        canvas.create_line(0, step_y * i, size_canvas_x, step_y * i)


draw_table()


def button_show_enemy():
    for i in range(0, s_x):
        for j in range(0, s_y):
            if enemy_ships[j][i] > 0:
                _id = canvas.create_rectangle(i * step_x, j * step_y, i * step_x + step_x, j * step_y + step_y,
                                             fill="red")
                list_ids.append(_id)


def button_begin_again():
    pass


# добавляем кнопки
b0 = Button(tk, text='Показать коробли противника', command=button_show_enemy)
# добавляем кнопки на панель и смещаем их чтобы они небыли на игровом поле
b0.place(x=size_canvas_x + 20, y=30)
# добавляем кнопки на панель и смещаем их чтобы они небыли на игровом поле
b1 = Button(tk, text="Начать заново!", command=button_begin_again)
b1.place(x=size_canvas_x + 20, y=70)


def add_to_all(event):
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
    print(ip_x, ip_y, '_type', _type)


canvas.bind_all('<Button-1>', add_to_all)  # левая кнопка мыши
canvas.bind_all('<Button-3>', add_to_all)  # правая кнопка мыши


def generate_enemy_ships():
    global enemy_ships
    ships_list = []
    # генерация короблей по размерам
    for i in range(0, ships):
        ships_list.append(random.choice([ships_len1, ships_len2, ships_len3]))
    print(ships_list)
    # подсчет сумарной длинны коробля
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
        print(enemy_ships)


generate_enemy_ships()

# цикл для работы нашего приложения
while app_running:
    if app_running:
        # обновление нашего окна
        tk.update_idletasks()
        tk.update()
    time.sleep(0.005)
