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
            <Input
                type='number'
                onChange={this.props.onChange}
                value={this.props.open} min={0} max={100}
                style={{marginLeft: "3px", marginRight: "3px"}}
            />
        )
    }
}

export default Valve;
