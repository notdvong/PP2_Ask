from functools import reduce

numbers = [1, 2, 3, 4, 5]
print(f"Original numbers: {numbers}\n")

#map Applies a function to every item in the list
# Here, we square every number
squared = list(map(lambda x: x**2, numbers))
print(f"Map (Squared): {squared}")

#filter Keeps only the items that return True for a condition
# Here, we keep only the even numbers
evens = list(filter(lambda x: x % 2 == 0, numbers))
print(f"Filter (Evens only): {evens}")

# reduce Applies a rolling computation to sequential pairs to reduce them to a single value
# Here, we multiply 1*2, then 2*3, then 6*4, then 24*5
product = reduce(lambda x, y: x * y, numbers)
print(f"Reduce (Product of all): {product}")