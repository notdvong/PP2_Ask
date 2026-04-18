#JSON is a syntax for storing and exchanging data.

#JSON is text, written with JavaScript object notation.
import json

#If you have a JSON string, you can parse it by using the json.loads() method which is called parsing

# some JSON:
x =  '{ "name":"John", "age":30, "city":"New York"}'

# parse x:
y = json.loads(x)

# the result is a Python dictionary:
print(y["age"])

#If you have a Python object, you can convert it into a JSON string by using the json.dumps() method which is called serialization
# a Python object (dict):
x = {
  "name": "John",
  "age": 30,
  "city": "New York"
}

# convert into JSON:
y = json.dumps(x)

# the result is a JSON string:
print(y)

#you can convert into json following types
print(json.dumps({"name": "John", "age": 30}))
print(json.dumps(["apple", "bananas"]))
print(json.dumps(("apple", "bananas")))
print(json.dumps("hello"))
print(json.dumps(42))
print(json.dumps(31.76))
print(json.dumps(True))
print(json.dumps(False))
print(json.dumps(None))

#indent parameter to define the numbers of indents, separators parameter to change the default separator
json.dumps(x, indent=4, separators=(". ", " = "))