#When you have imported the re module, you can start using regular expressions
import re

#The findall() function returns a list containing all matches
txt = "The rain in Spain"
x = re.findall("ai", txt)
print(x)

#Search for the first white-space character in the string
txt = "The rain in Spain"
x = re.search("\s", txt)

print("The first white-space character is located in position:", x.start())
#If no matches are found, the value None is returned

#The split() function returns a list where the string has been split at each match
txt = "The rain in Spain"
x = re.split("\s", txt)
print(x)

#The sub() function replaces the matches with the text of your choice
txt = "The rain in Spain"
x = re.sub("\s", "9", txt)
print(x)

#A Match Object is an object containing information about the search and the result
txt = "The rain in Spain"
x = re.search("ai", txt)
print(x) #this will print an object

#.span() returns a tuple containing the start-, and end positions of the match.
#.string returns the string passed into the function
#.group() returns the part of the string where there was a match

#examples

txt = "The rain in Spain"
x = re.search(r"\bS\w+", txt)
print(x.group())

txt = "The rain in Spain"
x = re.search(r"\bS\w+", txt)
print(x.string())

txt = "The rain in Spain"
x = re.search(r"\bS\w+", txt)
print(x.span())