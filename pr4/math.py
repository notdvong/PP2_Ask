#these are the built in fuction and there is nothing special about them
x = min(5, 10, 25)
y = max(5, 10, 25)

print(x)
print(y)

c = abs(-7.25)

print(c)

#Return the value of 4 to the power of 3
x = pow(4, 3)

print(x)

#in order to use more complicated methods we have to import math module
import math

x = math.sqrt(64) #square root of number 

print(x)

x = math.ceil(1.4) #rounds a number upwards to its nearest integer
y = math.floor(1.4) #rounds a number downwards to its nearest integer

print(x) # returns 2
print(y) # returns 1

#returns the value of PI (3.14...)
x = math.pi

print(x)

#1: 
degree = 15
#radians = degrees * (pi / 180)
radian = math.radians(degree)
print(f"Output radian: {radian:.6f}")
#2:
height = 5
base1 = 5
base2 = 6

area = ((base1 + base2) / 2) * height

print(f"Expected Output: {area}")
#3:
n = 4 # sides
s = 25 # length

area = (n * s**2) / (4 * math.tan(math.pi / n))

print(f"The area of the polygon is: {int(area)}")
#4:
base = 5
height = 6

area = float(base * height)

print(f"Expected Output: {area}")
