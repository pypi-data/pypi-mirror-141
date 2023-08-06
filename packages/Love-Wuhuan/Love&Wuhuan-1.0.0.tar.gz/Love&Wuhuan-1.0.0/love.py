import turtle
t=turtle

t.showturtle
t.color('red','pink')
t.begin_fill()
t.left(140)
t.forward(111.65)
for i in range(200):
       t. right(1)
       t.forward(1)

t.left(120)
for i in range(200):
       t. right(1)
       t.forward(1)
t.forward(111.65)
t.end_fill()
t.write('琳琳')
t.done()