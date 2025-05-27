# print(ord('XXXXX'), ord('00000'))
import time
import random


count = 1000000
flat = ''
for i in range(count):
    flat += random.choice(['X', '0'])


start = time.time()
sum_ord = sum(map(ord, flat))

result = sum_ord / count >= 68

# result = flat.count('X') >= int(count / 2)

print(time.time() - start)
