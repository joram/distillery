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
        if(this.state.enabled){
            return (
                <span>
                    Enabled <Button>Disable</Button>
                </span>
            )

        }
        return (
                <span>
                    Disabled <Button>Enable</Button>
                </span>
        )
    }
}

export default EnableButton;