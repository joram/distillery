from modules.base_module import BaseModule
import mock


def test_dfasdf():
    socket = mock.Mock()
    bm = BaseModule()
    bm._emit_value_update(socket, "A", "B", "C")

    socket.emit.assert_called_with('value_update', {'module': 'A', 'variable': 'B', 'value': 'C'}, broadcast=True, namespace='')
