import React from 'react';
import EnableButton from "./Enableable";
import {Label, Segment} from 'semantic-ui-react'


class Coolant extends React.Component {
    render() {
        return (
            <Segment>
                <Label className={"top attached"}>{this.props.name}</Label>
                <div>
                    <EnableButton/>
                </div>
            </Segment>
        );
    }
}

export default Coolant;
