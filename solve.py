import heapq
import math

def read_input():
    N = int(input())
    data = []
    for i in range(N):
        data.append([int(k) for k in input().split()] + [i])
    return N, data
  
def solve(N, data):
    # a visit has the following format: x, y, o, c, t, u, a, s, wait, maxshift, og_index
    current = [[200, 200, 0, 0, 0, 0, 0, 0, 0, 0, "N/A"], "end"]
    length = 0
    s = 1
    r = 1
    bestfound = current
    bestvalue = 0
    value = 0
    num_no_improvement = 0
    while num_no_improvement < 150:
        current, value, data, length = insert(data, current, value, length)
        if value > bestvalue:
            bestfound = current
            bestvalue = value
            r = 1
            num_no_improvement = 0
        else:
            num_no_improvement += 1
        #current, value = shake(r, s, current)
        s = s + r
        r = r + 1
        if s >= length:
            s = s - length
        if r == math.ceil(N/3):
            r = 1
    return bestfound, bestvalue
  
def insert(data, route, value, length):
    newroute, value, data, length = tryinsert(data, route, value, length)
    while newroute != route:
        route = newroute
        newroute, value, data, length = tryinsert(data, newroute, value, length)
    return newroute, value, data, length

def tryinsert(data, route, value, length):
    H = []
    for j in range(len(data)):
        x, y, o, c, u, t, indexj = data[j]
        bestshift = float('inf')
        bestwait = "none"
        bestarrival = "none"
        bestindex = "none"
        beststart = "none"
        bestoriginalindex = "none"
        for i in range(len(route)-1):
            k = i+1
            xi, yi, oi, ci, ti, ui, ai, si, waiti, maxshifti, ogi = route[i]
            if route[k] == "end":
                xk, yk, ck = 200, 200, 1440
            else:
                xk, yk, ok, ck, tk, uk, ak, sk, waitk, maxshiftk, ogk = route[k]
            c_ij = distance(xi, yi, x, y)
            c_jk = distance(x, y, xk, yk)
            c_ik = distance(xi, yi, xk, yk)
            possible_a = si + ti + c_ij
            possible_s = max(possible_a, o)
            if possible_a <= c and possible_s + t + c_jk <= ck:
              # if ride i start + ride i time + time from i to j <= j closing time
              # and ride j start + ride j time + time from j to k <= k closing time
              # then it might be possible to insert j
                wait = max(0, possible_s - possible_a)
                shift = c_ij + wait + t + c_jk - c_ik
                if ((route[k] != "end" and shift <= waitk + maxshiftk) or route[k] == "end") and shift < bestshift:
                    bestshift = shift
                    bestarrival = possible_a
                    beststart = possible_s
                    bestwait = wait
                    bestindex = i
                    bestoriginalindex = indexj
        if bestindex != "none":
            heapq.heappush(H, (-u**2/bestshift, [j, bestindex, bestarrival, beststart, bestwait, bestshift, bestoriginalindex]))
    if len(H) != 0:
        ratio, insertion = heapq.heappop(H)
        j, i, a, start, wait, shift, og_index = insertion
        x, y, o, c, u, t, og = data[j]
        value += u
        length += 1
        data.pop(j)
        route = updateafter(route, i, shift)
        maxshift = maxshiftupdate(route, i, c, start, t, x, y)
        route = updatebefore(route, i, wait, maxshift)
        return route[:i+1] + [[x, y, o, c, t, u, a, start, wait, maxshift, og_index]] + route[i+1:], value, data, length
    else:
        return route, value, data, length

def updateafter(route, i, shift):  
    earliershift = shift
    l = i+1
    while earliershift != 0 and l < len(route) - 1:
        x, y, o, c, t, u, a, s, wait, maxshift, og = route[l]
        route[l][8] = max(0, wait - earliershift)
        route[l][6] = a + earliershift
        earliershift = max(0, earliershift - wait)
        route[l][7] = s + earliershift
        route[l][9] = maxshift - earliershift
        l += 1
    return route
  
def updatebefore(route, i, wait, maxshift):
    nextwait = wait
    nextmaxshift = maxshift
    l = i
    while l != 0:
        x, y, o, c, t, u, a, s, wait, maxshift, og = route[l]
        route[l][9] = min(c - s, nextwait + nextmaxshift)
        nextwait = wait
        nextmaxshift = route[l][9]
        l -= 1
    return route

def maxshiftupdate(route, i, c, start, t, x, y):
    if i != len(route)-2:
        xk, yk, ok, ck, tk, uk, ak, sk, waitk, maxshiftk, ogk = route[i+1]
        return min(c - start, waitk + maxshiftk)
    else:
        return 1440 - (start + t) - distance(x, y, 200, 200)

                      
def distance(x1,y1,x2,y2):
    return math.ceil(math.sqrt((x2-x1)**2 + (y2-y1)**2))

# def shake(r, s, route):
#     ...
      
def main():
    N, data = read_input()
    route = [[200, 200, 0, 0, 0, 0, 0, 0, 0, 0, "N/A"], "end"]
    print(insert(data, route, 0, 0))

if __name__ == '__main__':
    main()
