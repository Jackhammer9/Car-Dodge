import turtle
import random
import time
from tkinter import *

def RunGame(difficulty):
    if difficulty == "Easy":
        factor = 1
    elif difficulty == 'Medium':
        factor = 0.85
    else:
        factor = 0.65

    root.destroy()

    Obstructions = []

    try:
        with open('highscore.txt' , 'r') as f:
            high_score = int(f.read())
            f.close()
    except:
        high_score = 0
        with open('highscore.txt' , 'w') as f:
            f.write(str(0))
            f.close()

    class Delay:
        def __init__(self):
            self.StartTime = time.time()

        def Wait(self , delay , func):
            if time.time() >= self.StartTime + delay:
                func()
                self.StartTime = time.time()

    class MatchTimer:
        def __init__(self):
            self.StartTime = time.time()

        def GetTime(self):
            return time.time() - self.StartTime

        def EndMatch(self):
            self.EndTime = self.GetTime()

        def GetNetTime(self):
            return self.EndTime

    shapes = ['circle' , 'square' , 'triangle' , 'turtle']
    colors = ['red' , 'blue' , 'yellow' , 'pink' , 'dark blue' , 'brown']

    def CreateObstruction():
        shape = random.choice(shapes)
        color = random.choice(colors)
        obstruct = turtle.Turtle()
        obstruct.ht()
        obstruct.speed(0)
        obstruct.penup()
        obstruct.color(color)
        obstruct.shape(shape)
        obstruct.shapesize(3)
        obstruct.goto(random.randint(-200 , 200) , 350)
        obstruct.st()
        Obstructions.append(obstruct)


    win = turtle.Screen()
    win.screensize(300,300)
    win.bgcolor('dark gray')
    win.title('Car Dodge')

    barrier_left = turtle.Turtle()
    barrier_left.shape('square')
    barrier_left.penup()
    barrier_left.speed(0)
    barrier_left.shapesize(40,8)
    barrier_left.goto(-300,0)
    barrier_left.color('black')

    barrier_right = turtle.Turtle()
    barrier_right.shape('square')
    barrier_right.penup()
    barrier_right.speed(0)
    barrier_right.shapesize(40,8)
    barrier_right.goto(300,0)
    barrier_right.color('black')

    def left():
        if car.xcor() > -200:
            car.goto(car.xcor()-10 , car.ycor())

    def right():
        if car.xcor() < 200:
            car.goto(car.xcor()+10 , car.ycor())

    win.listen()
    win.onkeypress(left , 'a')
    win.onkeypress(right , 'd')

    roadmark1 = turtle.Turtle()
    roadmark1.shape('square')
    roadmark1.color('white')
    roadmark1.shapesize(4,1)
    roadmark1.penup()
    roadmark1.goto(0 , -200)
    roadmark1.speed(0)

    roadmark2 = turtle.Turtle()
    roadmark2.shape('square')
    roadmark2.color('white')
    roadmark2.shapesize(4,1)
    roadmark2.penup()
    roadmark2.sety(roadmark1.ycor() + 200)
    roadmark2.speed(0)

    roadmark3 = turtle.Turtle()
    roadmark3.shape('square')
    roadmark3.color('white')
    roadmark3.shapesize(4,1)
    roadmark3.penup()
    roadmark3.sety(roadmark2.ycor() + 200)
    roadmark3.speed(0)

    pen = turtle.Turtle()
    pen.penup()
    pen.ht()
    pen.color('white')
    pen.speed(0)
    pen.goto(-340,220)
    pen.pensize(8)

    car = turtle.Turtle()
    car.penup()
    car.shape('square')
    car.color('dark green')
    car.shapesize(4,2)
    car.speed(0)
    car.goto(0,-150)

    clock = Delay()

    win.tracer(0)

    timer = MatchTimer()

    run = True
    while run:
        speed = (timer.GetTime()/30)
        if roadmark1.ycor() <= -320:
            roadmark1.sety(320)
        roadmark1.goto(roadmark1.xcor() , roadmark1.ycor() - 3)

        if roadmark2.ycor() <= -320:
            roadmark2.sety(320)
        roadmark2.goto(roadmark2.xcor() , roadmark2.ycor() - 3)

        if roadmark3.ycor() <= -320:
            roadmark3.sety(320)
        roadmark3.goto(roadmark3.xcor() , roadmark3.ycor() - 3)

        clock.Wait( factor , CreateObstruction)

        for obstruction in Obstructions:
            obstruction.goto(obstruction.xcor() , obstruction.ycor() - 3 - speed)
            if obstruction.ycor() <= -320:
                obstruction.reset()
                Obstructions.remove(obstruction)
                obstruction.ht()
            elif obstruction.distance(car) <= 50:
                run = False
                timer.EndMatch()


        car.goto(car.xcor() , car.ycor())
        pen.goto(pen.xcor() , pen.ycor())
        pen.clear()
        pen.color(random.choice(colors))
        pen.write(f'Score: {int(timer.GetTime())} \nHigh Score: {high_score} ' , font=("Calibri", 12, "bold"))
        win.update()
        
    if timer.GetNetTime() > high_score:
        high_score = int(timer.GetNetTime())
        with open('highscore.txt' , 'w') as f:
            f.write(str(high_score))
            f.close()

    pen.write(f'Score: {int(timer.GetTime())} \nHigh Score: {high_score} \n Game Over! ' , font=("Calibri", 12, "bold"))

    win.mainloop()

root = Tk()
root.title('Car Dodge Game Settings')
root.geometry('900x300')
root.config(bg='black')

heading = Label(text='Choose Game Difficulty ')
heading.grid(row=0,column=0,padx=275)

heading.config(bg='black' , fg='green' , font=('Calibri' , 24))

options = [
    'Easy' ,
    "Medium" ,
    'Hard'
]

clicked = StringVar()
clicked.set('Easy')

drop = OptionMenu( root , clicked , *options)
drop.config(width=20)
drop.grid(row=1,column=0 , padx=400 , pady=75)

button = Button(root , width=20 , height=3 , text='run' , bg='red' , fg='white' , command=lambda:RunGame(clicked.get()))
button.grid(row = 2 , column = 0 , padx=400 , pady=10)

root.mainloop()