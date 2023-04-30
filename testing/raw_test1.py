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
btest = open("brutetest.txt", "w+")

line = fd.readline()

cur_time = timer()

while (len(line) > 0):

    n = int(line)
    rect = []

    # input rectangles
    for i in range(n):
        x1, y1, x2, y2 = map(int, fd.readline().split())

        # create rectangle array
        rect.append([x1, y1, x2, y2])

    m = int(fd.readline())
    for i in range(m):
        x1, x2 = map(int, fd.readline().split())

        count = 0
        # bruteforce
        for r in rect:
            if (r[0] <= x1 and x1 < r[2] and x2 >= r[1] and x2 < r[3]):
                count += 1

    btest.write(str(n) + " " + str((timer() - cur_time)*(10**9))+"\n")
    line = fd.readline()




