
# with open('test2.txt') as file:
#     data = file.read().split('\n')

# lenght = int(data[0])
# q_coord = list(map(int, data[1].split()))
# c_coord = list(map(int, data[2].split()))
# a, b = list(map(int, data[3].split()))

lenght = int(input())
q_coord = list(map(int, input().split()))
c_coord = list(map(int, input().split()))
a, b = list(map(int, input().split()))

result = 0
for i in range(lenght):

    c = c_coord[i]
    # d = ((c / 255) * (b - a) + a)
    d = ((c * (b - a)) / 255) + a if c != 0 else a
    result += d * q_coord[i]

print(int(result))
