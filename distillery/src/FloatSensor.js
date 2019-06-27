import React from 'react';
import {Icon} from 'semantic-ui-react'

class FloatSensor extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            floating: this.props.floating,
        }
    }

    render() {
        if (this.props.floating) {
            return <span>
                floating
                <Icon name={"arrow circle up"}/>
            </span>
        }
        return <span>
            not floating
            <Icon name={"arrow circle down"}/>
        </span>
    }
}

export default FloatSensor;
