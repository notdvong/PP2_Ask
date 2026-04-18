#To write to an existing file, you must add a parameter to the open() function:

#"a" - Append - will append to the end of the file

#"w" - Write - will overwrite any existing content
with open("demofile.txt", "a") as f:
  f.write("Now the file has more content!")

#open and read the file after the appending:
with open("demofile.txt") as f:
  print(f.read())

#Open the file "demofile.txt" and overwrite the content
with open("demofile.txt", "w") as f:
  f.write("Woops! I have deleted the content!")

#open and read the file after the overwriting:
with open("demofile.txt") as f:
  print(f.read())