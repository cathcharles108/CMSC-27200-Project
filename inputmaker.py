# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import random
import math
import numpy as np

def distance(x,y):
    return math.sqrt((x-200)**2 + (y-200)**2)

def makeinput(N):
    x, y, u, o, c, t = [], [], [], [], [], []
    for i in range(N):
        while True:
            x1 = random.randint(0, 400)
            y1 = random.randint(0, 400)
            u1 = random.randint(1, 27200)
            o1 = random.randint(0, 1440)
            c1 = random.randint(o1,1440)
            test = int(1440 - c1 - distance(x1, y1))
            if test >= 1:
                    m = 1440 - o1
                    t1 = random.randint(c1-o1+1, m)
                    if 0 <= i <= 2**(int(math.log(N,2)) - 3) - 1:
                        if o1+t1 - c1 + 1 <= 30:
                            continue
                        u_new = u1 + 500
                        ulist = [int(np.ceil(u_new/3)) for _ in range(3)]
                        nested = [[] for _ in range(3)]
                        nested[0].append(random.randint(0, 400))
                        nested[0].append(random.randint(0, 400))
                        nested[0].append(random.randint(c1, o1+t1))
                        nested[0].append(random.randint(nested[0][-1], o1+t1))
                        nested[0].append(ulist[0])
                        nested[0].append(random.randint(1, nested[0][3] - nested[0][2]))
                        for j in range(2):
                            nested[j+1].append(random.randint(0, 400))
                            nested[j+1].append(random.randint(0, 400))
                            nested[j+1].append(random.randint(nested[j][3], o1+t1))
                            nested[j+1].append(random.randint(nested[j+1][-1], o1+t1))
                            nested[j+1].append(ulist[j+1])
                            nested[j+1].append(random.randint(1, nested[j+1][3] - nested[j+1][2]))
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
        print(f"{x[i]} {y[i]} {o[i]} {c[i]} {u[i]} {t[i]}")

    # for i in range(N):
    #     while True:
    #         x1 = random.randint(0, 400)
    #         y1 = random.randint(0, 400)
    #         u1 = random.randint(1, 27200)
    #         o1 = random.randint(0, 1440)
    #         c1 = random.randint(o1,1440)
    #         test = int(1440-c1-distance(x1,y1))
    #         if (test >= 1):
    #             m = 1440 - o1
    #             t1 = random.randint(1, m)
    #             x.append(x1)
    #             y.append(y1)
    #             u.append(u1)
    #             o.append(o1)
    #             c.append(c1)
    #             t.append(t1)
    #             break
    #         else:
    #             continue
    #     with open("inputs/large3.in","a") as input_file:
    #         print(f"{x[i]} {y[i]} {o[i]} {c[i]} {u[i]} {t[i]}", file=input_file)
    #         input_file.close()

def readinput():
    N = int(input())
    # with open("inputs/large3.in", "w") as input_file:
    #     print(N, file=input_file)
    #     input_file.close()
    return N

def main():
    N = readinput()
    makeinput(N)
    # print("hello world")

if __name__ == '__main__':
    main()