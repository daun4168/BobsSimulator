# Import the extension module hello.
import helloworld
import time

st_time = time.time()
for i in range(1000):
    helloworld.sum_num(10000)
print(time.time() - st_time)


number = 10000
st_time = time.time()
for i in range(1000):
    num = 0
    for j in range(number + 1):
        num += i
print(time.time() - st_time)

