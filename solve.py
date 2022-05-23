import heapq
import math

def read_input():
    N = int(input())
    data = [[int(i) for i in input().split()] for _ in range(N)]
    return N, data
  
def solve(N, data):
    # a visit has the following format: x, y, o, c, t, u, a, maxshift
    current = [[200, 200, 0, 0, 0, 0, 0, 0], "end"]
    s = 1
    r = 1
    bestfound = current
    bestvalue = 0
    num_no_improvement = 0
    while num_no_improvement < 150:
        current, value, data, length = insert(data, current)
        if value > bestvalue:
            bestfound = current
            bestvalue = value
            r = 1
            num_no_improvement = 0
        else:
            num_no_improvement += 1
        current = shake(r, s, current)
        s = s + r
        r = r + 1
        if s >= length:
            s = s - length
        if r == math.ceil(N/3):
            r = 1
    return bestfound, bestvalue
  
def insert(data, route):
    newroute = tryinsert(data, route)
    while newroute != route:
      newroute = tryinsert(data, newroute)
    return newroute 

def tryinsert(data, route):
    H = []
    for j in range(len(data)):
        x, y, o, c, t, u = data[j]
        bestshift = float('inf')
        bestwait = "none"
        bestarrival = "none"
        bestindex = "none"
        bestmaxshift = "none"
        for i in range(len(route)-1):
            k = i+1
            xi, yi, oi, ci, ti, ui, ai, maxshifti = route[i]
            if route[k] == "end":
                xk, yk, ck = 200, 200, 1440
            else:
                xk, yk, ok, ck, tk, uk, ak, maxshiftk = route[k]
            c_ij = distance(xi, yi, x, y)
            c_jk = distance(x, y, xk, yk)
            c_ik = distance(xi, yi, xk, yk)
            si = math.ceil(max(ai, oi)) # s stands for ride service start (either next whole minute after arrival or opening time)
            if si + ti + c_ij <= c and math.ceil(max(si + ti + c_ij, o)) + t + c_jk <= ck:
              # if ride i start + ride i time + time from i to j <= j closing time
              # and ride j start + ride j time + time from j to k <= k closing time
              # then it might be possible to insert j
                possible_a = si + ti + c_ij
                possible_s = math.ceil(max(possible_a, o))
                wait = max(0, possible_s - possible_a)
                sk = math.ceil(max(ak, ok))
                waitk = max(0, sk - ak)
                shift = c_ij + wait + t + c_jk - c_ik
                if ((route[k] != "end" and shift <= waitk + maxshiftk) or route[k] == "end") and bestshift < shift:
                    bestshift = shift
                    bestarrival = possible_a
                    bestwait = wait
                    bestmaxshift = min(c - possible_s, waitk + maxshiftk)
                    bestindex = i
        if bestindex != "none":
            heapq.heappush(H, (-u**2/bestshift, [j, bestindex, bestarrival, bestwait, bestshift, bestmaxshift]))
    ratio, insertion = heapq.heappop(H)
    j, i, a, wait, shift, maxshift = insertion
    x, y, o, c, t, u = data[j]
    route = updatebefore(updateafter(route, i, shift), i, wait, maxshift)
    return route[:i+1] + [[x, y, o, c, t, u, a, maxshift]] + route[k:]

def updateafter(route, i, shift):  
    ...

def updatebefore(route, i, wait, maxshift):
    ...
                      
def distance(x1,y1,x2,y2):
    return math.sqrt((x2-x1)**2 + (y2-y1)**2)

def shake(r, s, route):
    ...
      
def main():
    N, data = read_input()
    output = solve(N, data)

if __name__ == '__main__':
    main()
