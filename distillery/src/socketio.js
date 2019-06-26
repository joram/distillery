import io from 'socket.io-client';
let socket = io('ws://localhost:5000');


export default socket;
