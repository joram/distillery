from button import Button


class FloatSensor(Button):

  def __init__(self, pin):
    Button.__init__(self, pin)

  def isFloating(self):
    return self.pressed
