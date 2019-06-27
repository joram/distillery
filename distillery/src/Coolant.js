import React from 'react';
import EnableButton from "./Enableable";
import {Label, Loader, Segment} from 'semantic-ui-react'
import socket from "./socketio";


class Coolant extends React.Component {

    constructor(props) {
        super(props);
        socket.on('value_update', this.update.bind(this));
        this.state = {
            enabled: null,
        }
    }

    update(data) {
        if(this.props.module === data.module){
            let state = this.state;
            state.enabled = data.variable === "enabled" ? data.value : state.enabled;
            this.setState(state);
        }
    }

    render() {
        let content = <div>
            <EnableButton enabled={this.state.enabled}/>
        </div>;

        if(this.state.enabled === null){
            content = <Loader>Loading</Loader>
        }

        return (
            <Segment>
                <Label className={"top attached"}>{this.props.name}</Label>
                {content}
            </Segment>
        );
    }
}

export default Coolant;
