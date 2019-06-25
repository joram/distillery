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
                    <EnableButton/>
                    <Valve/>
                    <FloatSensor/>
                </div>
            </Segment>
        );
    }
}

export default Bilge;
