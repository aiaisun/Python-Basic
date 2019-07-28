# times=float(0)
#
# while times < 10:
#     print(" " * (times-( times /2 - 1 ) ), "*" * (2 * times + 1) )
#     times = times + 1


cycle=0

while cycle <10:
    stars = 10 - (cycle + 1 )
    blank = 2 * cycle + 1
    print(" " * stars + "*" * blank)
    cycle = cycle + 1
