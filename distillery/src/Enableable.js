import React from 'react';
import {Button} from 'semantic-ui-react'


class EnableButton extends React.Component {
    render() {
        return (
            <span>
                <Button className={"left attached"}>Enable</Button>
                <Button className={"right attached"}>Disable</Button>
            </span>
        )
    }
}

export default EnableButton;