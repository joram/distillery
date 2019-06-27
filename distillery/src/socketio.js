import io from 'socket.io-client';
let socket = io('ws://localhost:5000');

function log_message(data){
    let {module, variable, value } = data;
    console.log(`${module}:\t${variable}=${value}`);
}

socket.on('value_update', log_message);

export default socket;
