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