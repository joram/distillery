import io from 'socket.io-client';

let url = window.location.origin;
if(url === "http://localhost:3000"){url = "ws://localhost:5000"}
if(url.startsWith("https://")){url = url.replace("https://", "ws://")}
if(url.startsWith("http://")){url = url.replace("http://", "ws://")}
console.log(url);
let socket = io(url);

function log_message(data){
    let {module, variable, value } = data;
    console.log(`${module}:\t${variable}=${value}`);
}

socket.on('value_update', log_message);

export default socket;
