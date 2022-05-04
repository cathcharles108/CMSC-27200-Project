# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import random

def makeinput(N):
    x, y, u, o, c, t = [], [], [], [], [], []
    for i in range(N):
        x.append(random.randint(0, 401))
        y.append(random.randint(0, 401))
        u.append(random.randint(1, 27201))
        o.append(random.randint(0, 14401))

def readinput():
    N = int(input())
    return N

def main():
    N = readinput()
    makeinput(N)

if __name__ == '__main__':
    main()

