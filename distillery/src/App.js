import React from 'react';
import './App.css';
import Bilge from "./Bilge";
import Coolant from "./Coolant";
import TemperatureGraph from "./TemperatureGraph";
import {Container, SegmentGroup} from "semantic-ui-react";

class App extends React.Component {

    render(){
        return (
            <Container>
                <SegmentGroup horizontal>
                    <Coolant name={"Coolant Loop"}/>
                    <Bilge name={"Wash Bilge"} variable_name={"wash_bilge"} style={{marginLeft: "3em"}}/>
                </SegmentGroup>
                <TemperatureGraph name={"Temperature"}/>
            </Container>
        );
    }
}

export default App;
