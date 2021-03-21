from matplotlib.widgets import Button
from mpl_toolkits.axes_grid1.inset_locator import InsetPosition
from random import shuffle, randrange
import matplotlib.pyplot as plt
from tkinter.messagebox import showerror
import numpy as np
import tkinter as tk
import random
import string


def show_everything(w, h):
    def gen():
        def make_maze(w, h):
            vis = [[0] * w + [1] for _ in range(h)] + [[1] * (w + 1)]
            ver = [["|  "] * w + ['|'] for _ in range(h)] + [[]]
            hor = [["+--"] * w + ['+'] for _ in range(h + 1)]

            def walk(x, y):
                vis[y][x] = 1

                d = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
                shuffle(d)
                for (xx, yy) in d:
                    if vis[yy][xx]: continue
                    if xx == x: hor[max(y, yy)][x] = "+  "
                    if yy == y: ver[y][max(x, xx)] = "   "
                    walk(xx, yy)

            walk(randrange(w), randrange(h))

            s = ""
            for (a, b) in zip(hor, ver):
                s += ''.join(a + ['\n'] + b + ['\n'])
            return s

        with open("GM.txt", "w") as text_file:
            print(make_maze(w, h), file=text_file)

        string_maze = open("GM.txt", "r")
        orig = string_maze.read()

        char1 = 'S'
        char2 = 'E'

        while char1 == char2:  # #check if both char are equal
            char2 = random.choice(string.ascii_lowercase)

        ran_pos1 = random.randint(0, len(orig) - 1)  # random index1
        ran_pos2 = random.randint(0, len(orig) - 1)  # random index2

        while ran_pos1 == ran_pos2:  # check if both pos are equal
            ran_pos2 = random.randint(0, len(orig) - 1)

        orig_list = list(orig)
        orig_list[ran_pos1] = char1
        orig_list[ran_pos2] = char2
        mod = ''.join(orig_list)
        with open("Ready.txt", "w") as text_file:
            print(''.join(''.join(row) for row in mod), file=text_file)

        maze = []

        with open("Ready.txt", 'r') as file:
            for line in file:
                line = line.rstrip()
                row = []
                for c in line:
                    if c == ' ':
                        row.append(1)  # spaces are 1s
                    elif c == 'S':
                        row.append(2)  # start and end are 1s

                    elif c == 'E':
                        row.append(2)

                    else:
                        row.append(0)  # walls are 0s

                maze.append(row)

        maze = list(filter(None, maze))
        npa = np.asarray(maze, dtype=np.float32)
        return npa

    def solver():
        location = []
        hasNoEnd = True

        infile = open("Ready.txt", 'r')
        maze = [list(row) for row in
                infile.read().splitlines()]
        infile.close()

        for y in range(0, len(maze)):
            for x in range(0, len(maze[y])):
                if maze[y][x] == 'S':
                    location = [y, x]
                elif maze[y][x] == 'E':
                    hasNoEnd = False

        if len(location) == 0:
            raise Exception("No start cell found, check your input file")
        if hasNoEnd:
            raise Exception("Maze has no end, unsolvable.")

        tick(maze, location[0], location[1])
        print("\n\n")
        dump(maze)

        maze = []

        with open("SM.txt", 'r') as file:
            for line in file:
                line = line.rstrip()
                row = []
                for c in line:
                    if c == ' ':
                        row.append(1)  # spaces are 1s
                    elif c == 'x':
                        row.append(1)  # spaces are 1s

                    elif c == '.':
                        row.append(2)  # spaces are 1s

                    else:
                        row.append(0)  # walls are 0s

                maze.append(row)

        maze = list(filter(None, maze))
        npa = np.asarray(maze, dtype=np.float32)
        return npa

    def dump(maze):
        with open("SM.txt", "w") as text_file:
            print('\n'.join(''.join(row) for row in maze), file=text_file)

    def tick(maze, y, x):
        dump(maze)
        print("\n")
        if maze[y][x] in (' ', 'S'):
            maze[y][x] = 'x'

            if (tick(maze, y, x + 1) or tick(maze, y - 1, x) or
                    tick(maze, y, x - 1) or tick(maze, y + 1, x)):
                maze[y][x] = '.'
                return True
        elif maze[y][x] == 'E':
            return True
        return False

    def show_solver(event):
        plt.subplot(212)
        plt.title("A Solved Maze")
        plt.imshow(solver())
        plt.gca().axes.get_yaxis().set_visible(False)
        plt.gca().axes.get_xaxis().set_visible(False)

    fig, ax = plt.subplots()
    fig.canvas.set_window_title('Amazed py matplot')

    plt.subplot(211)
    plt.title("A Generated Maze")
    plt.imshow(gen())
    plt.gca().axes.get_yaxis().set_visible(False)
    plt.gca().axes.get_xaxis().set_visible(False)

    button_ax = plt.axes([0, 0, 1, 1])
    ip = InsetPosition(ax, [0.35, 0.4, 0.3, 0.1])  # posx, posy, width, height
    button_ax.set_axes_locator(ip)
    solve_button = Button(button_ax, 'Check Solution')
    solve_button.on_clicked(show_solver)

    plt.show()


def display1():
    num1 = e1.get()
    num2 = e2.get()
    try:
        num1 = int(num1)
        num2 = int(num2)
    except ValueError:
        showerror('Non-Int Error', 'Please enter an integer')
    else:
        show_everything(num1, num2)


root = tk.Tk()
root.title('Select Width and Height')

tk.Label(root,
         text="Width").grid(row=0)
tk.Label(root,
         text="Height").grid(row=1)

e1 = tk.Entry(root)
e2 = tk.Entry(root)

e1.grid(row=0, column=1)
e2.grid(row=1, column=1)

tk.Button(root,
          text='Show',
          command=root.quit).grid(row=3, column=0, sticky=tk.W, pady=4)

wt = 300
ht = 120


ws = root.winfo_screenwidth()
hs = root.winfo_screenheight()


xz = (ws/2) - (wt/2)
yz = (hs/2) - (ht/2)

root.geometry('%dx%d+%d+%d' % (wt, ht, xz, yz))
root.mainloop()

display1()
