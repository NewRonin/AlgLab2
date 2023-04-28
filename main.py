import copy


def closestBinPow(x):
    i = 1
    while (i < x):
        i *= 2
    return i

def makeTree(a):
    for i in range(len(a), closestBinPow(len(a))):
        a.append(0)

    b = [0] * (len(a) * 2)

    for i in range(len(a)):
        b[i + len(a) - 1] = a[i]
    for i in range(len(a)-2, -1, -1):
        b[i] = b[2 * i + 1] + b[2 * i + 2]

    return b

#[l, r]
def requestTree(l, r, n, b):
    sum = 0
    l += n
    r += n

    while (l != 0):
        if (l % 2 != 0):
            sum += b[l - 1]
        if (r % 2 == 0):
            sum += b[r - 1]

        if (l == r):
            break

        l = l // 2
        r = (r - 1) // 2

    return sum

def requestTreeLinks(x1, x2, tree_mod_links):
    tree = tree_mod_links[x1]
    print(tree)

    i = x2
    sum = tree[i]
    while i != 0:
        i = i // 2
        sum += tree[i]

    return sum


def getNode(node, x, l, r, b):
    print(node, l, r)

    if (l == r):
        print(l)
        return b[node]
    else:
        mid = (l + r) // 2
        if (x <= mid):
            return b[node] + getNode(node * 2, x, l, mid, b)
        else:
            return b[node] + getNode((node * 2) + 1, x, mid+1, r, b)



#[l, r)
def changeMod(node, begin, end, l, r, x):
    print(node, l, r)
    if (l > r):
        return 0

    if (l == begin and r == end):
        mod[node] += x

    else:
        mid = (begin + end) // 2
        changeMod(node * 2, begin, mid, l, min(r, mid), x)
        changeMod(node * 2 + 1, mid + 1, end, max(l, mid+1), r, x)



n = int(input())
points = []
x_bar = set([])
y_bar = set([])
y_events = []
dict = {}

counter = 0
for i in range(n):

    x1, y1, x2, y2 = map(int, input().split())
    x_bar.add(x1)
    y_bar.add(y1)
    x_bar.add(x2)
    y_bar.add(y2)

    y_events.append([y1, y2, 1])
    y_events.append([y1, y2, -1])

    points.append([x1, y1])
    points.append([x2, y2])

x_bar = list(x_bar)
y_bar = list(y_bar)
x_bar.sort()
y_bar.sort()

y_events.sort(key=lambda x: (-x[2], x[1] if x[2] < 0 else x[0], x[0] if x[2] < 0 else x[1]))

print(y_bar)
print(y_events)
for i in range(len(y_bar)):
    dict[y_bar[i]] = i

for i in range(len(y_events)):
    y_events[i][0] = dict.get(y_events[i][0])
    y_events[i][1] = dict.get(y_events[i][1])
print(y_events)

nodes = len(x_bar) - 1
tree_links = [None] * len(x_bar)
tree_mod_links = [None] * len(x_bar)
print(tree_mod_links)
b = makeTree(x_bar)
mod = [0] * len(b)

counter = 0
for event in y_events:
    x1 = event[0]
    x2 = event[1]

    changeMod(0, 0, len(mod) - 1, x1, x2, event[2])
    tree_links[counter] = copy.deepcopy(b)
    tree_mod_links[counter] = copy.deepcopy(mod)
    counter += 1


n = int(input())
for i in range(n):
    x1, x2 = map(int, input().split())
    x1 = dict.get(x1)
    x2 = dict.get(x2)
    print(requestTreeLinks(x1 - 1, x2 - 1, tree_mod_links))