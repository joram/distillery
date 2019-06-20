from button import Button


class FloatSensor(Button):

    def __init__(self, pin):
        Button.__init__(self, pin)
    
    def pressed(self):
        print("floating")

    def unpressed(self):
        print("not floating")

    def is_floating(self):
        return self.is_pressed
