import turtle
turtle.shape("turtle")
turtle.pencolor("#9fdbed")
step = 200
turtle.penup()
turtle.setpos(-1*step/2, step/2)
turtle.pendown()

turtle.forward(200)
turtle.right(90)
turtle.forward(200)
turtle.right(90)
turtle.forward(200)
turtle.right(90)
turtle.forward(180)
turtle.right(90)
turtle.forward(20)

turtle.getscreen().mainloop()