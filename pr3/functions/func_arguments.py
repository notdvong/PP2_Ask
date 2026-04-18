#we give information to function using arguments, it is the "Emil" and "Tobias" here, but the parameter is the fname
def my_function(fname):
  print(fname + " Refsnes")

my_function("Emil")
my_function("Tobias")
my_function("Linus")

#you can add as many arguments as you want,just separate them with a comma
def my_function(fname, lname):
  print(fname + " " + lname)

my_function("Emil", "Refsnes")

#If the function is called without an argument, it uses the default value which is inside the 'name' here
def my_function(name = "friend"):
  print("Hello", name)

my_function("Emil")
my_function("Tobias")
my_function()
my_function("Linus")

#you can send arguments by key =value, in this case order of the arguments does not matter
def my_function(animal, name):
  print("I have a", animal)
  print("My", animal + "'s name is", name)

my_function(name = "Buddy", animal = "dog")

#you can send and receive any type of data including lists,dict,string,tuple etc
def my_function(fruits):
  for fruit in fruits:
    print(fruit)

my_fruits = ["apple", "banana", "cherry"]
my_function(my_fruits)


#To specify positional-only arguments, add , / after the arguments. You cannot use keyword here
def my_function(name, /):
  print("Hello", name)

my_function("Emil")

#To specify that a function can have only keyword arguments, add *, before the arguments
def my_function(*, name):
  print("Hello", name)

my_function(name = "Emil")

