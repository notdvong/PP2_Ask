#Lists, tuples, dictionaries, and sets are all iterable objects. They are iterable containers which you can get an iterator from
mytuple = ("apple", "banana", "cherry")
myit = iter(mytuple)

print(next(myit))
print(next(myit))
print(next(myit))
#strings are also iterable
mystr = "banana"
myit = iter(mystr)

print(next(myit))
print(next(myit))
print(next(myit))
print(next(myit))
print(next(myit))
print(next(myit))

#using for to iterate through an object
mytuple = ("apple", "banana", "cherry")

for x in mytuple:
  print(x)
#The for loop actually creates an iterator object and executes the next() method for each loop

#Create an iterator that returns numbers, starting with 1, and each sequence will increase by one (returning 1,2,3,4,5 etc.)
class MyNumbers:
  def __iter__(self):
    self.a = 1
    return self

  def __next__(self):
    x = self.a
    self.a += 1
    return x

myclass = MyNumbers()
myiter = iter(myclass)

print(next(myiter))
print(next(myiter))
print(next(myiter))
print(next(myiter))
print(next(myiter))




#A generator function is a special type of function that returns an iterator object. Instead of using return to send back a single value, generator functions use yield to produce a series of results over time. The function pauses its execution after yield, maintaining its state between iterations.
def fun(max):
    cnt = 1
    while cnt <= max:
        yield cnt
        cnt += 1

#examples
ctr = fun(5)
for n in ctr:
    print(n)

sq = (x*x for x in range(1, 6))
for i in sq:
    print(i)
#generators are also very memory efficient so in large data bases they are really useful because it will take almost no RAM

#1:
def square_gen(N):
    for i in range(N + 1):
        yield i ** 2

for num in square_gen(5):
    print(num)

#2:
def even_gen(n):
    for i in range(0, n + 1, 2):
        yield str(i)

n = int(input("Enter n: "))
print(", ".join(even_gen(n)))
#3:
def div_gen(n):
    for i in range(n + 1):
        if i % 3 == 0 and i % 4 == 0:
            yield i
for val in div_gen(100):
    print(val)
#4:
def squares(a, b):
    for i in range(a, b + 1):
        yield i * i
for val in squares(3, 6):
    print(val)
#5:
def countdown(n):
    while n >= 0:
        yield n
        n -= 1
for num in countdown(5):
    print(num)
