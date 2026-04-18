#The filter() function creates a list of items for which a function returns True
numbers = [1, 2, 3, 4, 5, 6, 7, 8]
odd_numbers = list(filter(lambda x: x % 2 != 0, numbers))
print(odd_numbers)

#Keep only the even numbers
numbers = [1, 5, 8, 10, 13, 16, 20]
evens = list(filter(lambda x: x % 2 == 0, numbers))
print(evens)

#Keep only words longer than 3 characters
words = ["apple", "it", "banana", "is", "cherry", "a"]
long_words = list(filter(lambda w: len(w) > 3, words))

print(long_words)