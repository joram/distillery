import React from 'react';
import {Icon} from 'semantic-ui-react'


class FloatSensor extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            floating: false,
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
