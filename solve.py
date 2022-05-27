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
        current, value, data, length = shake(r, s, current, value, data, length)
        s = s + r
        r = r + 1
        if s > length:
            s = s - length
        if r >= length:
            r = 1
        if r == math.ceil(N / 3):
            r = 1
        if bestfound[-1] != "end":
            print("here")
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
        for i in range(len(route) - 1):
            k = i + 1
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
            heapq.heappush(H, (
            -u ** 2 / bestshift, [j, bestindex, bestarrival, beststart, bestwait, bestshift, bestoriginalindex]))
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
        return route[:i + 1] + [[x, y, o, c, t, u, a, start, wait, maxshift, og_index]] + route[
                                                                                          i + 1:], value, data, length
    else:
        return route, value, data, length


def updateafter(route, i, shift):
    earliershift = shift
    l = i + 1
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
    if i != len(route) - 2:
        xk, yk, ok, ck, tk, uk, ak, sk, waitk, maxshiftk, ogk = route[i + 1]
        return min(c - start, waitk + maxshiftk)
    else:
        return 1440 - (start + t) - distance(x, y, 200, 200)


def distance(x1, y1, x2, y2):
    return math.ceil(math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2))


def shake(r, s, route, value, data, length):
    rte = route.copy()
    begin = rte.pop(0)
    final = rte.pop(-1)
    l = len(rte)
    start = s - 1
    end = (s - 2 + r) % l
    if start <= end:
        valuedeleted = sum([rte[j][5] for j in range(start, end + 1)])
        for j in range(start, end + 1):
            data.append([rte[j][0], rte[j][1], rte[j][2], rte[j][3], rte[j][5], rte[j][4], rte[j][10]])
        del rte[start: end + 1]
        rte = [begin] + rte + [final]
        rte = updateshake(rte, start, end, length)
        # while m < len(route):
        #     xm, ym, om, cm, tm, um, am, sm, waitm, maxshiftm, ogm = route[m]
        #     if m >= 1:
        #         x, y, o, c, t, u, a, s, wait, maxshift, og = route[m - 1]
        #     else:
        #         x, y, o, c, t, u, a, s, wait, maxshift, og = 200, 200, 0, 0, 0, 0, 0, 0, 0, 0, "N/A"
        #     dist = distance(x, y, xm, ym)
        #     newam = s + t + dist
        #     shift = newam - am
        #     newsm = max(newam, om)
        #     newwaitm = max(0, newsm - newam)
        #     newmaxshiftm = maxshiftm + shift
        #     route[m] = [xm, ym, om, cm, tm, um, newam, newsm, newwaitm, newmaxshiftm, ogm]
        #     m += 1
        #if start > 0 and end + 1 != length:
             #route = updatebefore(route, start, route[start+1][8], route[start+1][9])
    else:
        valuedeleted = sum([rte[j][5] for j in range(start, l)] + [rte[j][5] for j in range(0, end + 1)])
        for j in range(start, l):
            data.append([rte[j][0], rte[j][1], rte[j][2], rte[j][3], rte[j][5], rte[j][4], rte[j][10]])
        for j in range(0, end + 1):
            data.append([rte[j][0], rte[j][1], rte[j][2], rte[j][3], rte[j][5], rte[j][4], rte[j][10]])
        del rte[start: l]
        del rte[0: end + 1]
        rte = [begin] + rte + [final]
        rte = updateshake(rte, end + 1, end, length)
        # while m < len(route):
        #     xm, ym, om, cm, tm, um, am, sm, waitm, maxshiftm, ogm = route[m]
        #     x, y, o, c, t, u, a, s, wait, maxshift, og = route[m - 1]
        #     dist = distance(x, y, xm, ym)
        #     newam = s + t + dist
        #     shift = am - newam
        #     newsm = max(newam, om)
        #     newwaitm = max(0, newsm - newam)
        #     newmaxshiftm = maxshiftm + shift
        #     route[m] = [xm, ym, om, cm, tm, um, newam, newsm, newwaitm, newmaxshiftm, ogm]
        #     m += 1
    return rte, value - valuedeleted, data, len(rte) - 2

def updateshake(route, start, end, length):
    m = start + 1
    if len(route) == 2:
        return route
    if end + 1 != length:
        while m < len(route) - 1:
            xm, ym, om, cm, tm, um, am, sm, waitm, maxshiftm, ogm = route[m]
            x, y, o, c, t, u, a, s, wait, maxshift, og = route[m - 1]
            dist = distance(x, y, xm, ym)
            newam = s + t + dist
            newsm = max(newam, om)
            newwaitm = max(0, newsm - newam)
            if newsm == sm:
                route[m] = [xm, ym, om, cm, tm, um, newam, newsm, newwaitm, maxshiftm, ogm]
                route = updatebefore(route, m-1, newwaitm, maxshiftm)
                break
            if m == len(route) - 2:
                newmaxshiftm = 1440 - (sm + tm) - distance(x, y, 200, 200)
                route[m] = [xm, ym, om, cm, tm, um, newam, newsm, newwaitm, newmaxshiftm, ogm]
                route = updatebefore(route, m - 1, newwaitm, newmaxshiftm)
            m += 1
    else:
        x, y, o, c, t, u, a, s, wait, maxshift, og = route[m - 1]
        newmaxshift = 1440 - (start + t) - distance(x, y, 200, 200)
        route[m-1][9] = newmaxshift
        if len(route) >= 2:
            route = updatebefore(route, m-2, wait, maxshift)
    return route

def main():
    N, data = read_input()
    x, value = solve(N, data)
    # x = (insert(data, route, 0, 0))[0]
    print(x)
    print(f"value = {value}")
    l = len(x)
    res = []
    for i in range(1, l - 1):
        res.append(x[i][-1])
    print(l - 2)
    print(*res)

if __name__ == '__main__':
    main()
