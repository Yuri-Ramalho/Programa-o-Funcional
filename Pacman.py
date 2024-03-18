from random import choice
from turtle import *
from freegames import floor, vector
from tkinter import messagebox

# Monad
class ScoreMonad:
    def __init__(self, score):
        self.score = score

    def bind(self, func):
        return ScoreMonad(func(self.score))

# Função para atualizar a pontuação
def update_score(score):
    return score + 1

state = ScoreMonad(0)
path = Turtle(visible=False)
writer = Turtle(visible=False)
aim = vector(5, 0)
pacman = vector(-40, -80)
ghosts = [
    [vector(-180, 160), vector(5, 0)],
    [vector(-180, -160), vector(0, 5)],
    [vector(100, 160), vector(0, -5)],
    [vector(100, -160), vector(-5, 0)],
]

# Mapa original
tiles = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0,
    0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0,
    0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0,
    0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0,
    0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0,
    0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0,
    0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0,
    0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0,
    0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0,
    0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
]

total_balls = tiles.count(1)

def square(x, y):
    """Desenha um quadrado usando o caminho em (x, y)."""
    path.up()
    path.goto(x, y)
    path.down()
    path.begin_fill()

    for count in range(4):
        path.forward(20)
        path.left(90)

    path.end_fill()

def offset(point):
    """Retorna o deslocamento do ponto em blocos."""
    x = (floor(point.x, 20) + 200) // 20
    y = (180 - floor(point.y, 20)) // 20
    index = int(x + y * 20)
    return index

def valid(point):
    """Retorna Verdadeiro se o ponto for válido em blocos."""
    index = offset(point)

    if tiles[index] == 0:
        return False

    index = offset(point + 19)

    if tiles[index] == 0:
        return False

    return point.x % 20 == 0 or point.y % 20 == 0

def world():
    """Desenha o mundo usando path."""
    bgcolor('black')
    path.color('blue')

    for index, tile in enumerate(tiles):
        if tile == 1:
            x = (index % 20) * 20 - 200
            y = 180 - (index // 20) * 20
            square(x, y)
            path.up()
            path.goto(x + 10, y + 10)
            path.dot(2, 'white')

def move():
    """Move o pacman e todos os fantasmas"""
    global state

    writer.undo()
    writer.write(state.score)

    clear()

    if valid(pacman + aim):
        pacman.move(aim)

    index = offset(pacman)

    if tiles[index] == 1:
        tiles[index] = 2
        # Atualiza a pontuação encapsulada no monad
        state = state.bind(update_score)
        x = (index % 20) * 20 - 200
        y = 180 - (index // 20) * 20
        square(x, y)
        path.up()
        path.goto(x + 10, y + 10)

    up()
    goto(pacman.x + 10, pacman.y + 10)
    dot(20, 'yellow')

    for point, course in ghosts:
        if valid(point + course):
            point.move(course)
        else:
            # List Comprehension para gerar opções de movimento dos fantasmas
            options = [vector(x, y) for x in [5, -5, 0] for y in [5, -5, 0] if not (x == 0 and y == 0)]
            plan = choice(options)
            course.x = plan.x
            course.y = plan.y

        up()
        goto(point.x + 10, point.y + 10)
        dot(20, 'red')

    for point, _ in ghosts:
        if abs(pacman - point) < 20:
            messagebox.showinfo("Fim de Jogo", "Você perdeu o jogo!")
            bye() 
            return 

    if state.score == total_balls:
        messagebox.showinfo("Parabéns!", "Você ganhou o jogo!")
        bye() 
        return 

    ontimer(move, 100) 

def change(x, y):
    """Muda o alvo do pacman se válido."""
    # Closure
    def inner():
        if valid(pacman + vector(x, y)):
            aim.x = x
            aim.y = y
    return inner

def setup_screen():
    """Configura a tela do Turtle."""
    screen = Screen()
    screen.setup(420, 420)
    screen.bgcolor('black')
    screen.tracer(False)

def continuation_function():
    """Função de continuação que configura o jogo e o inicia."""
    setup_screen()
    hideturtle()
    writer.goto(180, 180)
    writer.color('white')
    writer.write(state.score)
    listen()

    # Função lambda
    onkey(change(5, 0), 'Right')
    onkey(change(-5, 0), 'Left')
    onkey(change(0, 5), 'Up')
    onkey(change(0, -5), 'Down')
    world()
    move()
    done()

# Iniciar o jogo
continuation_function()
mainloop()