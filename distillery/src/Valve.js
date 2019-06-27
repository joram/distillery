import React from 'react';
import {Input} from 'semantic-ui-react'


class Valve extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            value: this.props.open,
        }
    }

    render() {
        return (
            <Input type='number' value={this.props.open} max={5} style={{marginLeft: "3px", marginRight: "3px"}}/>
        )
    }
}

export default Valve;
