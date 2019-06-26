import React from 'react';
import EnableButton from "./Enableable";
import Valve from "./Valve";
import {Label, Segment} from 'semantic-ui-react'
import FloatSensor from "./FloatSensor";


class Bilge extends React.Component {
    render() {
        return (
            <Segment>
                <Label className={"top attached"}>{this.props.name}</Label>
                <div>
                    <EnableButton  name={this.props.variable_name+"_enable_button"}/>
                    <Valve  name={this.props.variable_name+"_valve"}/>
                    <FloatSensor name={this.props.variable_name+"_float_sensor"}/>
                </div>
            </Segment>
        );
    }
}

export default Bilge;
