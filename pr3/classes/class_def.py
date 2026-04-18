#A Class is like an object constructor, or a "blueprint" for creating objects.
class MyClass:
  x = 5
#Create an object named p1, and print the value of x
p1 = MyClass()
print(p1.x)

#Delete the p1 object
del p1

#Create three objects from the MyClass class
p1 = MyClass()
p2 = MyClass()
p3 = MyClass()

print(p1.x)
print(p2.x)
print(p3.x)
