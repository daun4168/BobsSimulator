def say_hello_to(name):
    print("Hello %s!" % name)

def sum_num(int number):
    cdef int num, i
    num = 0
    for i in range(number + 1):
        num += i
    return num