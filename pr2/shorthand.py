#If you have only one statement to execute, you can put it on the same line as the if statement.

a = 5
b = 2
if a > b: print("a is greater than b")
#You still need the colon : after the condition.

a = 2
b = 330
print("A") if a > b else print("B")


a = 10
b = 20
bigger = a if a > b else b
print("Bigger is", bigger)


a = 330
b = 330
print("A") if a > b else print("=") if a == b else print("B")


username = ""
display_name = username if username else "Guest"
print("Welcome,", display_name)
# While shorthand if statements can make code more concise, avoid overusing them for complex conditions. For readability, use regular if-else statements when dealing with multiple lines of code or complex logic.
