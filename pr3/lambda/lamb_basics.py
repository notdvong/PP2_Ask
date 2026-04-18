#A lambda function can take any number of arguments, but can only have one expression
#Add 10 to argument a, and return the result. 
x = lambda a : a + 10
print(x(5))

#it can take multiple arguments as said before
x = lambda a, b : a * b
print(x(5, 6))

#it is useful as a anonymous function inside another function
def myfunc(n):
  return lambda a : a * n

mydoubler = myfunc(2)

print(mydoubler(11))

#more examples of usage
def myfunc(n):
  return lambda a : a * n

mydoubler = myfunc(2)
mytripler = myfunc(3)

print(mydoubler(11))
print(mytripler(11))