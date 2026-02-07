#When you compare two values, the expression is evaluated and Python returns the Boolean answer:
print(10 > 9)
print(10 == 9)
print(10 < 9)


a = 200
b = 33

if b > a:
  print("b is greater than a")
else:
  print("b is not greater than a")

#The bool() function allows you to evaluate any value, and give you True or False in return,
print(bool("Hello"))
print(bool(15))

#Almost any value is evaluated to True if it has some sort of content.
bool("abc")
bool(123)
bool(["apple", "cherry", "banana"])
