# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import random
import math

def distance(x1,y1,x2,y2):
    return math.sqrt((x2-x1)**2 + (y2-y1)**2)

def makeinput(N):
    x, y, u, o, c, t = [], [], [], [], [], []
    for i in range(N):
        while True:
            x1 = random.randint(0, 400)
            y1 = random.randint(0, 400)
            u1 = random.randint(1, 27200)
            o1 = random.randint(0, 1440)
            c1 = random.randint(o1,1440)
            test = int(1440 - c1 - distance(x1, y1, 200, 200))
            if test >= 1:
                    m = 1440 - o1
                    t1 = random.randint(c1-o1, m)
                    if 0 <= i <= 2**(int(math.log(N,2)) - 3) - 1:
                        if o1+t1 - c1  <= 50:
                            continue
                        unew = u1 + 500
                        d1 = random.randint(1, unew + 500)
                        d2 = random.randint(d1, unew + 500)
                        ulist = [d1, d2 - d1, unew + 500 - d2]
                        nested = [[] for _ in range(3)]
                        l = o1+t1 - c1
                        nested[0].append(pointwithin(x1, y1, l/12)[0])
                        nested[0].append(pointwithin(x1, y1, l/12)[1])
                        nested[0].append(random.randint(c1+int(l/12), c1+3*int(l/12)))
                        nested[0].append(random.randint(nested[0][-1], c1 + 3*int(l/12)))
                        nested[0].append(ulist[0])
                        nested[0].append(random.randint(1, nested[0][3] - nested[0][2] + 1))
                        nested[1].append(pointwithin(nested[0][0], nested[0][1], l/12)[0])
                        nested[1].append(pointwithin(nested[0][0], nested[0][1], l/12)[1])
                        nested[1].append(random.randint(c1+4*int(l/12), c1+6*int(l/12)))
                        nested[1].append(random.randint(nested[1][-1], c1+6*int(l/12)))
                        nested[1].append(ulist[1])
                        nested[1].append(random.randint(1, nested[1][3] - nested[1][2] + 1))
                        nested[2].append(pointwithin(nested[1][0], nested[1][1], l/12)[0])
                        nested[2].append(pointwithin(nested[1][0], nested[1][1], l/12)[1])
                        nested[2].append(random.randint(c1+7*int(l/12), c1+9*int(l/12)))
                        nested[2].append(random.randint(nested[2][-1], c1 +9*int(l/12)))
                        nested[2].append(ulist[2])
                        nested[2].append(random.randint(1, nested[2][3] - nested[2][2] + 1))
                        for k in range(3):
                            x.append(nested[k][0])
                            y.append(nested[k][1])
                            o.append(nested[k][2])
                            c.append(nested[k][3])
                            u.append(nested[k][4])
                            t.append(nested[k][5])
                    x.append(x1)
                    y.append(y1)
                    u.append(u1)
                    o.append(o1)
                    c.append(c1)
                    t.append(t1)
                    break
            else:
                continue
    randomlist = list(range(1, N+1))
    random.shuffle(randomlist)
    for i in randomlist:
        print(f"{x[i]} {y[i]} {o[i]} {c[i]} {u[i]} {t[i]}")
        with open("input/large3.in","a") as input_file:
            print(f"{x[i]} {y[i]} {o[i]} {c[i]} {u[i]} {t[i]}", file=input_file)
            input_file.close()

def pointwithin(x, y, d):
    while True:
        xnew = random.randint(0, 400)
        ynew = random.randint(0, 400)
        if distance(x, y, xnew, ynew) < int(d):
            return [xnew, ynew]
          
def readinput():
    N = int(input())
    with open("input/large3.in", "w") as input_file:
        print(N, file=input_file)
        input_file.close()
    return N

def main():
    N = readinput()
    makeinput(N)
    # print("hello world")

if __name__ == '__main__':
    main()