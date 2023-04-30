# Лабораторная работа №2 (АиСД)

# Цель работы

Для поставленной задачи реализовать три алгоритма:

- **Алгоритм перебора**
- **Алгоритм на карте**
- **Алгоритм на дереве**

Выяснить в зависимости от объема начальных данных и точек, какой алгоритм эффективнее.

# Контест

Был пройден под учётной записью — **madudarev@edu.hse.ru** 

Последняя попытка: 30 апр 2023, 09:29:35

# Реализация

Файлы с полным кодом алгоритмов будут на [GitHub](https://github.com/NewRonin/alg-lab2) и в приложенном архиве, ниже приведены основные “куски” реализации.

## 1. Bruteforce алгоритм

**Сложность:**

Подготовка — **O($1$) (нет подготовки)**

Ответ на запрос — **O($N$)**

**Суть:**

Ничего необычного из себя алгоритм не представляет, при запросе считываем прямоугольники и интересующие точки организуем полный перебор.

Полный код:

```python
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
```

## 2. Map алгоритм

**Сложность:**

Подготовка — **O($N^3$)** 

Ответ на запрос — **O($logN$)**

**Суть:**

Сжимаем координаты, строим на основе всех прямоугольников матрицу, последовательно по ним проходимся и вносим информацию в таблицу. 

При запросе конвертируем за логарифм поступившие координаты в сжатые и обращаемся к элементу таблицы.

**Сжатие координат при запросе:**

```python
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
```

**Сжатие координат при построении:**

```python
#fill dicts
for i in range(len(y_bar)):
    dict_y[y_bar[i]] = i

for i in range(len(x_bar)):
    dict_x[x_bar[i]] = i

#compress values in events
for i in range(len(events)):
    events[i][0] = dict_x.get(events[i][0])
    events[i][1] = dict_y.get(events[i][1])
    events[i][2] = dict_x.get(events[i][2])
    events[i][3] = dict_y.get(events[i][3])
```

**Создание и заполнение таблицы:**

```python
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
```

## 3. Персистентное дерево отрезков

**Сложность:**

Подготовка — **O($NlogN$)** 

Ответ на запрос — **O($logN$)**

**Сложность реализации через индексы:**

Подготовка — **O($N^2$)** 

Ответ на запрос — **O($logN$)**

При моём подходе деревья представляют собой массив, проход по которому осуществляется через подсчёт индексов. Минус такой реализации, который я осознал только на момент написания отчёта — полное копирование при создании массива вершин. Это ухудшает сложность до **O($N^2$)** , что всё ещё лучше **O($N^3$)**  и никак не влияет на время ответов на запрос, но при реализации полноценной структуры данных для узлов можно улучшить время работы алгоритма. 

**Суть:**

Сжимаем координаты, строим дерево для $y$ координат. Формируем события на основе поданных на вход прямоугольников. Реализуем персистентное дерево: формируем массив вершин, проходимся по событиям, изменяем модификаторы в дереве на основе событий, записываем или перезаписываем результат в массив вершин. 

При запросе обращаемся к массиву вершин по $x$, к номеру узла в версии дерева по $y$.

**Создание событий:**

```python
		#sort events by 1.x 2.mod 3.y1 or y2, depends on mod value
    y_events.sort(key=lambda x: (x[3], -x[2], x[1] if x[2] < 0 else x[0], x[0] if x[2] < 0 else x[1]))

    #compressing values, replacing coordinates on compressed ones {
    for i in range(len(y_bar)):
        dict[y_bar[i]] = i

    for i in range(len(x_bar)):
        dict_x[x_bar[i]] = i

    for i in range(len(y_events)):
        y_events[i][0] = dict.get(y_events[i][0])
        y_events[i][1] = dict.get(y_events[i][1])
        y_events[i][3] = dict_x.get(y_events[i][3])
    #}
```

**Создание персистентного дерева:**

```python
#create persistent tree based on events
    for event in y_events:
        x1 = event[0]
        x2 = event[1]

        changeMod(1, 0, len(y_bar) - 1, x1, x2 - 1, event[2])
        tree_mod_links[event[3]] = copy.deepcopy(mod)
```

**Изменение модификатора:**

```python
#Changes module of found child
#works on [l, r] actually
def changeMod(node, begin, end, l, r, x):

    if (l > r):
        return 0

    if (l == begin and r == end):
        mod[node] += x

    else:
        mid = (begin + end) // 2
        changeMod(node * 2, begin, mid, l, min(r, mid), x)
        changeMod(node * 2 + 1, mid + 1, end, max(l, mid+1), r, x)
```

**Обработка запроса:**

```python
def requestTreeLinks(x1, x2, tree_mod_links, n):
    #Find tree based on input x
    tree = tree_mod_links[x1]

    #Find child with number of input y
    return getNode(1, x2, 0, n - 1, tree)
```

**Поиск узла по номеру в дереве:**

```python
def getNode(node, x, l, r, b):

    if (l == r):
        return b[node]
    else:
        mid = (l + r) // 2
        if (x <= mid):
            return b[node] + getNode(node * 2, x, l, mid, b)
        else:
            return b[node] + getNode((node * 2) + 1, x, mid+1, r, b)
```

# Тестирование

Подробно исходный код тестов, их вывод можно посмотреть [тут](https://github.com/NewRonin/alg-lab2/tree/main/testing) или в архиве. 

Также для удобства есть xlsx файл [сравнения](https://github.com/NewRonin/alg-lab2/blob/main/results.xlsx) результатов работы этих трёх алгоритмов по времени.

**Код генерации данных для тестирования:**

```python
fd = open("buf.txt", "w+")

#picked randomly for +- representative sample
n = 10000
m = 100

for i in range(10, n, 10):
    fd.write(str(i // 10) + "\n")

    for j in range(0, (i // 10) * 10, 10):
				# formula according to lab2.docx
        fd.write(str(10* i)+ " " + str(10 * i) + " " + str(10*(2*i - j)) + " " + str(10*(2*i - j))+"\n")

    fd.write(str(m) + "\n")
    for j in range(m):
				# formula according to lab2.docx
        x = int((9109 * j)**31 % (20*i))
        fd.write(str(x) + " " + str(x)+"\n")

fd.close()
```

## Результаты тестирования:

![image (1).png](%D0%9B%D0%B0%D0%B1%D0%BE%D1%80%D0%B0%D1%82%D0%BE%D1%80%D0%BD%D0%B0%D1%8F%20%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%B0%20%E2%84%962%20(%D0%90%D0%B8%D0%A1%D0%94)%2074ec5ea9b81f458ea811717075aab788/image_(1).png)

**Анализ графика:**

В целом, из графика очевидно, что озвученная в цели работы оценка сложности верна. На больших данных **второй алгоритм** ведёт себя просто отвратительно и, честно говоря, если вы заглянете в [brutetest.txt](https://github.com/NewRonin/AlgLab2/blob/main/testing/brutetest.txt), то увидите, что мне даже пришлось прервать процесс тестирования, так как до дедлайна оставались считанные часы, а работало всё очень медленно. **Третий алгоритм** действительно ****показывает наилучшее время работы при $N>10^2$, что для меня удивительно, так как в процессе тестирования учитывается и время на подготовку данных. Мной ожидалось, что **полный перебор** будет лидером по времени работы, однако из графика видно, что его общее время работы растёт значительно быстрее. Возможно это связано с тем, что данный алгоритм не производит сжатие координат.

**Вывод:**

Даже визуально можно наблюдать, что реализация через персистентное дерево является самой эффективной по времени. Данный график разве что не отражает то, что при последующих запросах в каждом из представленных на нём случаях полный перебор станет работать значительно хуже, чем алгоритм на карте.  Отсюда можно сделать вывод, что практически всегда стоит использовать третий алгоритм, более того, мою реализацию можно даже значительно улучшить, как я писал выше. Возможно, если не рассматривать персистентное дерево, под ряд специфических задач будет уместно использовать первый алгоритм заместо второго, так как он не требует такого огромного количества памяти и очень прост в реализации. Поэтому второй алгоритм явно проигрывает остальным.