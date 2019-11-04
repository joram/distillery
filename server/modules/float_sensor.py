from modules.button import Button


class FloatSensor(Button):

    def __init__(self, pin, on_float=None, on_drop=None):
        self.on_float = on_float
        self.on_drop = on_drop
        Button.__init__(self, pin)
    
    def pressed_callback(self):
        if self.on_float is not None:
            print("floating %s" % self.pin)
            self.on_float()

    def unpressed_callback(self):
        if self.on_drop is not None:
            print("not floating %s" % self.pin)
            self.on_drop()

    @property
    def is_floating(self):
        return self.is_pressed
