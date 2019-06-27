import React from 'react';
import EnableButton from "./Enableable";
import Valve from "./Valve";
import {Label, Loader, Segment} from 'semantic-ui-react'
import FloatSensor from "./FloatSensor";
import socket from "./socketio";


class Bilge extends React.Component {
    constructor(props) {
        super(props);
        socket.on('value_update', this.update.bind(this));
        this.state = {
            enabled: null,
            floating: null,
            open: "",
        }
    }

    update(data) {
        if(this.props.module === data.module){
            let state = this.state;
            state.enabled = data.variable === "enabled" ? data.value : state.enabled;
            state.floating = data.variable === "floating" ? data.value : state.floating;
            state.open = data.variable === "open" ? data.value : state.open;
            this.setState(state);
        }
    }

    render() {
        let content = <div>
            <EnableButton enabled={this.state.enabled}/>
            <Valve open={this.state.open}/>
            <FloatSensor floating={this.state.floating}/>
        </div>;

        if(this.state.enabled === null || this.state.floating === null || this.state.open === ""){
            content = <Loader>Loading</Loader>
        }

        return (
            <Segment>
                <Label className={"top attached"}>{this.props.name}</Label>
                { content }
            </Segment>
        );
    }
}

export default Bilge;
