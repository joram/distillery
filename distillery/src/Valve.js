import React from 'react';
import {Input} from 'semantic-ui-react'


class Valve extends React.Component {
    render() {
        return (
            <Input type='number' max={5} style={{marginLeft: "3px", marginRight: "3px"}}/>
        )
    }
}

export default Valve;
