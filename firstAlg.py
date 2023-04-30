
n = int(input())
rect = []

#input rectangles
for i in range(n):

    x1, y1, x2, y2 = map(int, input().split())

    # create rectangle array
    rect.append([x1, y1, x2, y2])


m = int(input())
for i in range(m):
    x1, x2 = map(int, input().split())

    count = 0
    #bruteforce
    for r in rect:
        if (r[0] <= x1 and x1 < r[2] and x2 >= r[1] and x2 < r[3]):
            count += 1

    print(count, end = " ")
