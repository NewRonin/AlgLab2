
#Find closest compressed value for input coordiante
def compressValue(v, v_bar):

    low = 0
    high = len(v_bar) - 1

    while low <= high:
        mid = (low + high)//2
        if (v == v_bar[mid]):
            return mid
        elif (v > v_bar[mid]):
            low = mid + 1
        else:
            high = mid - 1

        if low > high:
            return low - 1

n = int(input())
points = []
x_bar = set([])
y_bar = set([])
dict = {}
dict_x = {}
events = []

#input rectangles
for i in range(n):

    x1, y1, x2, y2 = map(int, input().split())
    x_bar.add(x1)
    y_bar.add(y1)
    x_bar.add(x2)
    y_bar.add(y2)

    # create events
    events.append([x1, y1, x2, y2])

#sort dots
x_bar = list(x_bar)
y_bar = list(y_bar)
x_bar.sort()
y_bar.sort()

#fill dicts
for i in range(len(y_bar)):
    dict[y_bar[i]] = i

for i in range(len(x_bar)):
    dict_x[x_bar[i]] = i

#compress values in events
for i in range(len(events)):
    events[i][0] = dict_x.get(events[i][0])
    events[i][1] = dict.get(events[i][1])
    events[i][2] = dict_x.get(events[i][2])
    events[i][3] = dict.get(events[i][3])

#create cross table
matrix = []
for i in range(len(x_bar)):
    matrix.append([])
    for j in range(len(y_bar)):
        matrix[i].append(0)

#fill maxtrix for all compressed cases
for event in events:
    for i in range(event[0], event[2]):
        for j in range(event[1], event[3]):
            matrix[i][j] += 1

n = int(input())
ans = ""
for i in range(n):
    x1, x2 = map(int, input().split())

    if dict_x.get(x1) == None:
        x1 = x_bar[compressValue(x1, x_bar)]
    if dict.get(x2) == None:
        x2 = y_bar[compressValue(x2, y_bar)]

    x1 = dict_x.get(x1)
    x2 = dict.get(x2)
    ans += str(matrix[x1][x2]) + " "

print(ans[:-1])

