# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import random
import math

def distance(x,y):
    return math.sqrt((x-200)**2 + (y-200)**2)

def makeinput(N):
    x, y, u, o, c, t = [], [], [], [], [], []
    for i in range(N):
        while True:
            x1 = random.randint(0, 401)
            y1 = random.randint(0, 401)
            u1 = random.randint(1, 27201)
            o1 = random.randint(0, 1441)
            c1 = random.randint(o1,1441)
            test = int(1441-c1-distance(x1,y1))
            if (test >= 1):
                m = min(c1-o1, 1441-o1)
                t1 = random.randint(1, m)  
                x.append(x1)
                y.append(y1)
                u.append(u1)
                o.append(o1)
                c.append(c1)
                t.append(t1)
                break
            else:
                continue
        with open("inputs/small1.in","a") as input_file:
            print(f"{x[i]} {y[i]} {o[i]} {c[i]} {u[i]} {t[i]}", file=input_file)
            input_file.close()

def readinput():
    N = int(input())
    with open("inputs/small1.in", "w") as input_file:
        print(N, file=input_file)
        input_file.close()
    return N

def main():
    N = readinput()
    makeinput(N)

if __name__ == '__main__':
    main()
