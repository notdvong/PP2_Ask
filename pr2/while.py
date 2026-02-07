#With the while loop we can execute a set of statements as long as a condition is true.
i = 1
while i < 6:
  print(i)
  i += 1

#remember to increment i, or else the loop will continue forever.
i = 1
while i < 6:
  print(i)
  if i == 3:
    break
  i += 1



i = 0
while i < 6:
  i += 1
  if i == 3:
    continue
  print(i)


i = 1
while i < 6:
  print(i)
  i += 1
else:
  print("i is no longer less than 6")
#The else block will NOT be executed if the loop is stopped by a break statement.
