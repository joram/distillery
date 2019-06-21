from modules.button import Button


class FloatSensor(Button):

    def __init__(self, pin, on_float=None, on_drop=None):
        self.on_float = on_float
        self.on_drop = on_drop
        Button.__init__(self, pin)
    
    def pressed(self):
        if self.on_float is not None:
            self.on_float()

    def unpressed(self):
        if self.on_drop is not None:
            self.on_drop()

    def is_floating(self):
        return self.is_pressed
