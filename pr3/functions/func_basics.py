#thats how you define the function 
def my_function():
  print("Hello from a function")

my_function() #to call a function you have write its name 


def fahrenheit_to_celsius(fahrenheit):
  return (fahrenheit - 32) * 5 / 9

print(fahrenheit_to_celsius(77))
print(fahrenheit_to_celsius(95))
print(fahrenheit_to_celsius(50))
#you can turn repetitive code into reusable function 


def get_greeting():
  return "Hello from a function"

print(get_greeting())
#you can return values and when the function reaches return it stops executing