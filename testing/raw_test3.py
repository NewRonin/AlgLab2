import copy
from timeit import default_timer as timer

fd = open("buf.txt", "w+")

n = 10000
m = 100

for i in range(10, n, 10):
    fd.write(str(i // 10) + "\n")

    for j in range(0, (i // 10) * 10, 10):
        fd.write(str(10* i)+ " " + str(10 * i) + " " + str(10*(2*i - j)) + " " + str(10*(2*i - j))+"\n")

    fd.write(str(m) + "\n")
    for j in range(m):
        x = int((9109 * j)**31 % (20*i))
        fd.write(str(x) + " " + str(x)+"\n")

fd.close()

#BRUTEFORCE TEST
fd = open("buf.txt", "r")
ttest = open("treetest.txt", "w+")

line = fd.readline()

while (len(line) > 0):

    # Find closest compressed value for input coordiante
    def compressValue(v, v_bar):

        low = 0
        high = len(v_bar) - 1

        while low <= high:
            mid = (low + high) // 2
            if (v == v_bar[mid]):
                return mid
            elif (v > v_bar[mid]):
                low = mid + 1
            else:
                high = mid - 1

            if low > high:
                return low - 1


    # Building a tree (actually we don't use THIS one, later we create an empty one with same size)
    def makeTree(a, v, begin, end, b):

        if (begin == end):
            b[v] = a[begin]
        else:
            tm = (begin + end) // 2
            makeTree(a, v * 2, begin, tm, b)
            makeTree(a, v * 2 + 1, tm + 1, end, b)
            b[v] = b[v * 2] + b[v * 2 + 1]

        return b


    def requestTreeLinks(x1, x2, tree_mod_links, n):
        # Find tree based on input x
        tree = tree_mod_links[x1]

        # Find child with number of input y
        return getNode(1, x2, 0, n - 1, tree)


    def getNode(node, x, l, r, b):

        if (l == r):
            return b[node]
        else:
            mid = (l + r) // 2
            if (x <= mid):
                return b[node] + getNode(node * 2, x, l, mid, b)
            else:
                return b[node] + getNode((node * 2) + 1, x, mid + 1, r, b)


    # Changes module of found child
    # works on [l, r] actually
    def changeMod(node, begin, end, l, r, x):

        if (l > r):
            return 0

        if (l == begin and r == end):
            mod[node] += x

        else:
            mid = (begin + end) // 2
            changeMod(node * 2, begin, mid, l, min(r, mid), x)
            changeMod(node * 2 + 1, mid + 1, end, max(l, mid + 1), r, x)


    cur_time = timer()
    n = int(line)
    temp = n
    x_bar = set([])
    y_bar = set([])
    y_events = []
    dict = {}
    dict_x = {}
    counter = 0

    # case of no rectangles
    if (n == 0):
        m = fd.readline()
        for i in range(m):
            x1, x2 = map(int, input().split())
        ans = "0 " * m

    else:
        # input rectangles
        for i in range(n):
            x1, y1, x2, y2 = map(int, fd.readline().split())
            x_bar.add(x1)
            y_bar.add(y1)
            x_bar.add(x2)
            y_bar.add(y2)

            # create events
            y_events.append([y1, y2, 1, x1])
            y_events.append([y1, y2, -1, x2])

        # sort dots
        x_bar = list(x_bar)
        y_bar = list(y_bar)
        x_bar.sort()
        y_bar.sort()

        # sort events by 1.x 2.mod 3.y1 or y2, depends on mod value
        y_events.sort(key=lambda x: (x[3], -x[2], x[1] if x[2] < 0 else x[0], x[0] if x[2] < 0 else x[1]))

        # compressing values, replacing coordinates on compressed ones {
        for i in range(len(y_bar)):
            dict[y_bar[i]] = i

        for i in range(len(x_bar)):
            dict_x[x_bar[i]] = i

        for i in range(len(y_events)):
            y_events[i][0] = dict.get(y_events[i][0])
            y_events[i][1] = dict.get(y_events[i][1])
            y_events[i][3] = dict_x.get(y_events[i][3])
        # }

        # creating array of tree roots
        tree_mod_links = [None] * len(y_events)

        b = [0] * len(y_bar) * 2 ** 2

        for i in range(len(y_bar)):
            b[i] = y_bar[i]

        makeTree(y_bar, 1, 0, len(y_bar) - 1, b)

        # actual empty array we are working with
        mod = [0] * len(b)

        # create persistent tree based on events
        for event in y_events:
            x1 = event[0]
            x2 = event[1]

            changeMod(1, 0, len(y_bar) - 1, x1, x2 - 1, event[2])
            tree_mod_links[event[3]] = copy.deepcopy(mod)

        # answering actual requests
        n = int(fd.readline())
        ans = ""
        for i in range(n):
            x1, x2 = map(int, fd.readline().split())

            if dict_x.get(x1) == None:
                x1 = x_bar[compressValue(x1, x_bar)]
            if dict.get(x2) == None:
                x2 = y_bar[compressValue(x2, y_bar)]

            x1 = dict_x.get(x1)
            x2 = dict.get(x2)

            ans += str(requestTreeLinks(x1, x2, tree_mod_links, len(y_bar))) + " "

        # delete last " "

    ttest.write(str(temp) + " " + str((timer() - cur_time)*(10**9))+"\n")
    line = fd.readline()




