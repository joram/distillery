import React from 'react';
import {Button} from 'semantic-ui-react'


class EnableButton extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            enabled: this.props.enabled,
        }
    }


    render() {
        if(this.props.enabled){
            return (
                <>
                    Enabled <Button onClick={this.props.onClick} >Disable</Button>
                </>
            )

        }
        return (
                <>
                    Disabled <Button onClick={this.props.onClick} >Enable</Button>
                </>
        )
    }
}

export default EnableButton;