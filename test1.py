import math
# import textwrap

# with open('test1.txt') as file:
#     data = file.read().split('\n')


def my_wrap(text, width):
    return [text[i:i+width] for i in range(0, len(text), width)]


# n, m, x, y = list(map(int, data[0].split()))
n, m, x, y = list(map(int, input().split()))

height = n * x
height_one = height == 1
len_flat = x * y
half_flat = math.ceil(len_flat / 2)
data = []
for _ in range(height):
    data.append(
        [i.count('X') for i in my_wrap(input(), y)]
    )

# data = data[1:]

result = 0
for index in range(0, height, x):

    result += len(list(filter(
        lambda num: num >= half_flat,
        list(map(sum, zip(*data[index: index + x]))))))

print(result)
