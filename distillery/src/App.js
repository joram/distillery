import React from 'react';
import './App.css';
import Bilge from "./Bilge";
import Coolant from "./Coolant";
import TemperatureGraph from "./TemperatureGraph";
import {Container, Segment, SegmentGroup} from "semantic-ui-react";


function App() {
    return (
        <Container>
            <SegmentGroup horizontal>
                <Coolant name={"Coolant Loop"}/>
                <Bilge name={"Wash Bilge"} style={{marginLeft: "3em"}}/>
            </SegmentGroup>
            <TemperatureGraph name={"Temperature"}/>
        </Container>
    );
}

export default App;
