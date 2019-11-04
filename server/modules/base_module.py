
class BaseModule(object):

    def __init__(self):
        self.name = "base_module"

    def emit(self, socket):
        raise NotImplementedError()

    def process_action(self, action):
        raise NotImplementedError()

    def _emit_value_update(self, socket, module_name, variable_name, variable_value):
        msg = {
            "module": module_name,
            "variable": variable_name,
            "value": variable_value,
        }
        socket.emit('value_update', msg, broadcast=True, namespace="")

    def receive_action(self, module_name, data):
        if self.name == module_name:
            self.process_action(data)
