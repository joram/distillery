
class BaseModule(object):

    def emit(self, socket):
        raise NotImplementedError()

    def _emit_value_update(self, socket, module_name, variable_name, variable_value):
        msg = {
            "module": module_name,
            "variable": variable_name,
            "value": variable_value,
        }
        # print("emitting ", msg)
        socket.emit('value_update', msg, broadcast=True, namespace="")
