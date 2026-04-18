#Inheritance allows us to define a class that inherits all the methods and properties from another class.
#Parent class is the class being inherited from, also called base class.
#Child class is the class that inherits from another class, also called derived class.
class Person:
  def __init__(self, fname, lname):
    self.firstname = fname
    self.lastname = lname

  def printname(self):
    print(self.firstname, self.lastname)


class Student(Person):
  pass
#Now the Student class has the same properties and methods as the Person class.
x = Student("Mike", "Olsen")
x.printname()

#Use the Person class to create an object, and then execute the printname method:

x = Person("John", "Doe")
x.printname()
