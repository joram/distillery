import React from 'react';
import {Icon} from 'semantic-ui-react'
import socket from "./socketio"

class FloatSensor extends React.Component {

    constructor(props) {
        super(props);
        socket.on('float_sensor', this.update.bind(this));
        this.state = {
            floating: false,
        }
    }

    update(data) {
        console.log(data)
        if(this.props.name === data.name){
            console.log(`${this.props.name}: I should pay attention to this value`)
        } else {
            console.log(`${this.props.name}: Ignoring value`)
        }
    }


    render() {
        if (this.state.floating) {
            return <Icon name={"battery high"}/>
        }
        return <Icon name={"battery low"}/>
    }
}

export default FloatSensor;
