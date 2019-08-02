import turtle
times=0


turtle.shape("turtle")
turtle.pencolor("#9fdbed")
turtle.fillcolor("#9fdbed")

# color picker website

while times<6:

    turtle.left(60 * times)

    turtle.begin_fill()
    turtle.forward(200)
    turtle.left(120)
    turtle.forward(200)
    turtle.left(120)
    turtle.forward(200)
    turtle.home()
    turtle.end_fill()

    times = times + 1

turtle.getscreen().mainloop()