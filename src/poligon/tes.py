# https://stackoverflow.com/questions/67959894/how-to-sum-the-elements-of-2-lists-in-python
from timeit import Timer
from operator import add

a = list(range(31, 31+5*30, 5))
b = list(range(31, 31+3*30, 3))

print(a, b)

t2 = Timer("""[i+j for i,j in zip(a,b)]""", setup="a = list(range(1, 5*30, 5)); b = list(range(1, 3*30, 3))")
# vvvv winner vvv - almost as fast, less code
t3 = Timer("""from operator import add; list(map(add, a, b))""", setup="a = list(range(1, 5*30, 5)); b = list(range(1, 3*30, 3))")

c = map(add, a, b)
print("c:", c)

print(t2.timeit())
print(t3.timeit())
