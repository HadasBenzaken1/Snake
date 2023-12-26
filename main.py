from tkinter import *
import random

GAME_WIDTH= 700
GAME_HEIGHT=700
SPEED=150
SPACE_SIZE=75
BODY_PARTS= 3
SNAKE_COLOR="#0000FF"
FOOD_COLOR="#FF0000"
BACKGROUND_COLOR="#000000"

class Snake:
    
    def __init__(self):
        self.body_size=BODY_PARTS
        self.coordinates=[]
        self.squares=[]

        for i in range(0,self.body_size):
            self.coordinates.append([0,0])

        for x,y in self.coordinates:
            square= canvas.create_rectangle(x,y,x+SPACE_SIZE,y+SPACE_SIZE,fill=SNAKE_COLOR,tags="snake")
            self.squares.append(square)
    

class Food:

    def __init__(self):
        while True:
            x = random.randrange(0, int(GAME_WIDTH / SPACE_SIZE) - 1) * SPACE_SIZE
            y = random.randrange(0, int(GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE

            # Check if the new food coordinates overlap with the snake
            if (x, y) not in snake.coordinates:
                break

        self.coordinates = [x, y]
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")



def next_turn(snake,food):

    x,y=snake.coordinates[0]
    if direction=="up":
        y-=SPACE_SIZE
    elif direction=="down":
        y+=SPACE_SIZE
    elif direction=="left":
        x-=SPACE_SIZE
    elif direction=="right":
        x+=SPACE_SIZE

    snake.coordinates.insert(0,(x,y))
    square= canvas.create_rectangle(x,y,x+SPACE_SIZE,y+SPACE_SIZE,fill=SNAKE_COLOR)
    snake.squares.insert(0,square)

    if x== food.coordinates[0] and y==food.coordinates[1]:
        global score
        score+=1
        label.config(text="Score:{}".format(score))
        canvas.delete("food")
        food=Food()
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_colisiones(snake):
        game_over()
    else:
        window.after(SPEED,next_turn,snake,food)



def change_direction(new_direction):
    global direction

    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction
    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction
    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction
    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction

        

def check_colisiones(snake):
    x,y= snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH:
        return True
    if y < 0 or y >= GAME_HEIGHT:
        return True
    
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True
    
    return False



def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2,font=('consolas',70), text="GAME OVER", fill="red" ,tags="game over")
    


def restart_game():
    global snake, food, score, direction

    # Reset game variables to initial values
    canvas.delete(ALL)
    snake = Snake()
    food = Food()
    score = 0
    direction = 'down'
    label.config(text="Score:{}".format(score))
    next_turn(snake, food)



window=Tk()
window.title("Snake Game")
window.resizable(False,False)

score=0
direction='down'

# יצירת לוח המשחק
label=Label(window,text="Score:{}".format(score), font=('consolas',40))
label.pack()

canvas=Canvas(window,bg=BACKGROUND_COLOR,width=GAME_WIDTH,height=GAME_HEIGHT)
canvas.pack()

window.update()

#מיקום הלוח באמצע המסך
window_width=window.winfo_width()
window_height=window.winfo_height()
screem_width=window.winfo_screenwidth()
screem_height=window.winfo_screenheight()

x= int((screem_width/2)-(window_width/2))
y= int((screem_height/2)-(window_height/2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

snake=Snake()
food=Food()

restart_button = Button(window, text="Restart", command=restart_game, font=('consolas', 20))
restart_button.place(x=10, y=1)

next_turn(snake,food)
window.mainloop()