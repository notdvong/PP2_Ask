#multiple inheritance is a feature that allows a class to inherit attributes and methods from more than one parent class
class Camera:
    def take_photo(self):
        print("Photo taken!")
class Phone:
    def make_call(self):
        print("Calling...")
# Smartphone inherits from both Camera and Phone
class Smartphone(Camera, Phone):
    pass
my_phone = Smartphone()
my_phone.take_photo()  # From Camera
my_phone.make_call()   # From Phone

#more examples
class Sprite:
    #Base class for anything that can be drawn on screen.
    def draw(self):
        print("Drawing image at (x, y)")

class AIBehavior:
    #Logic for moving toward the player.
    def calculate_path(self):
        print("Calculating route to player...")

class Enemy(Sprite, AIBehavior):
    #An enemy that can be drawn AND has AI logic.
    def update(self):
        self.calculate_path()
        self.draw()

goblin = Enemy()
goblin.update()
