#The open() function takes two parameters; filename, and mode
#"r" - Read - Default value. Opens a file for reading, error if the file does not exist

#"a" - Append - Opens a file for appending, creates the file if it does not exist

#"w" - Write - Opens a file for writing, creates the file if it does not exist

#"x" - Create - Creates the specified file, returns an error if the file exists

f = open("demofile.txt")
print(f.read())

#You can also use the with statement when opening a file
with open("demofile.txt") as f:
  print(f.read())

#Return the 5 first characters of the file
with open("demofile.txt") as f:
  print(f.read(5))

#You can return one line by using the readline() method:
with open("demofile.txt") as f:
  print(f.readline())

#Loop through the file line by line
with open("demofile.txt") as f:
  for x in f:
    print(x)