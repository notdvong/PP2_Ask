class Person:
  def __init__(self, fname, lname):
    self.firstname = fname
    self.lastname = lname

  def printname(self):
    print(self.firstname, self.lastname)

#Use the Person class to create an object, and then execute the printname method:

x = Person("John", "Doe")
x.printname()

class Student(Person):
    def __init__(self, fname, lname):
        super().__init__(fname, lname) 

#When you add the __init__() function, the child class will no longer inherit the parent's __init__() function

class Student(Person):
  def __init__(self, fname, lname):
    Person.__init__(self, fname, lname)
#To keep the inheritance of the parent's __init__() function, add a call to the parent's __init__() function