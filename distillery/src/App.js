import React from 'react';
import './App.css';
import Bilge from "./Bilge";
import Coolant from "./Coolant";
import TemperatureGraph from "./TemperatureGraph";
import {Container, Grid} from "semantic-ui-react";


class App extends React.Component {

    render(){
        return (
            <Container>
                <Grid>
                    <Grid.Row>
                        <Grid.Column width={16}></Grid.Column>
                    </Grid.Row>
                    <Grid.Row>
                        <Grid.Column width={8}>
                            <Coolant name={"Coolant Loop"} module={"coolant"}/>
                        </Grid.Column>
                        <Grid.Column width={8}>
                            <Bilge name={"Wash Bilge"} module={"wash_bilge"} style={{marginLeft: "3em"}}/>
                        </Grid.Column>
                    </Grid.Row>
                </Grid>
                <TemperatureGraph name={"Temperature"}/>
            </Container>
        );
    }
}

export default App;
