#If you do not know how many arguments will be passed into your function, add a * before the parameter name. It will receive a tuple of arguments
def my_function(*kids):
  print("The youngest child is " + kids[2])

my_function("Emil", "Tobias", "Linus")

#Regular parameters must come before *args if you want multiple parameters
def my_function(greeting, *names):
  for name in names:
    print(greeting, name)

my_function("Hello", "Emil", "Tobias", "Linus")


#they are very usefull when you want to create a flexible function
def my_function(*numbers):
  total = 0
  for num in numbers:
    total += num
  return total

print(my_function(1, 2, 3))
print(my_function(10, 20, 30, 40))
print(my_function(5))

#If you do not know how many keyword arguments will be passed into your function, add two asterisks ** before the parameter name
#it will receive a dict of arguments this way 
def my_function(**kid):
  print("His last name is " + kid["lname"])

my_function(fname = "Tobias", lname = "Refsnes")

#Same way a regular parameters have to come first in order to use them both
def my_function(username, **details):
  print("Username:", username)
  print("Additional details:")
  for key, value in details.items():
    print(" ", key + ":", value)

my_function("emil123", age = 25, city = "Oslo", hobby = "coding")

