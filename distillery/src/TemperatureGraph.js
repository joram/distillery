import React from 'react';
import {Label, Segment, Button, Input} from 'semantic-ui-react'
import {Line} from 'react-chartjs-2';
import socket from "./socketio";

class TemperatureGraph extends React.Component {

    constructor(props) {
        super(props);
        socket.on('value_update', this.update.bind(this));
        this.calibration_value = 20;
        this.state = {
            temperatureData: {},
            labels: [],
        }
    }

    randomColor(){
        return '#'+
            Math.floor(Math.random()*16).toString(16)+
            Math.floor(Math.random()*16).toString(16)+
            Math.floor(Math.random()*16).toString(16)+
            Math.floor(Math.random()*16).toString(16)+
            Math.floor(Math.random()*16).toString(16)+
            Math.floor(Math.random()*16).toString(16);
    }

    update(data) {
        if(data.module === "temperature_probes") {
            let name = data.variable;
            let val = data.value;
            let state = this.state;
            let now = Date.now();
            let probeData = state.temperatureData[name];


            // add new probe
            if(probeData === undefined){
                state.temperatureData[name] = {
                    data: [],
                    label: name,
                    borderColor: this.randomColor(),
                    fill: false
                };
            }

            // add new data
            state.labels.push(now);
            state.temperatureData[name].data.push({x:now, y:val});

            // trim data
            var BUFFER = 30 * 60 * 1000; /* ms */
            let minDate = now - BUFFER;
            while(state.temperatureData[name].data.length >= 1){
                if(state.temperatureData[name].data[0].x < minDate){
                    state.temperatureData[name].data.shift();
                    continue
                }
                break
            }
            while(state.labels.length >= 1){
                if(state.labels[0] < minDate){
                    state.labels.shift();
                    continue
                }
                break
            }

            this.setState(state);
            this.forceUpdate()
        }
    }

    chartData() {
        return {
            update: Date.now(),
            labels: this.state.labels,
            datasets: Object.values(this.state.temperatureData),
        }
    }

    chartOptions() {

        return {
            elements: { point: { radius: 0 } },
            scales: {
                xAxes: [{
                    type: 'time',
                    time: {
                        displayFormats: {
                            quarter: 'MMM YYYY'
                        }
                    }
                }]
            },

            scaleShowGridLines: true,
            scaleGridLineColor: 'rgba(0,0,0,.05)',
            scaleGridLineWidth: 1,
            scaleShowHorizontalLines: true,
            scaleShowVerticalLines: true,
            bezierCurve: true,
            bezierCurveTension: 0.4,
            pointDot: true,
            pointDotRadius: 0,
            pointDotStrokeWidth: 0,
            pointHitDetectionRadius: 20,
            datasetStroke: true,
            datasetStrokeWidth: 2,
            datasetFill: true,
            // legendTemplate: '<ul class=\"<%=name.toLowerCase()%>-legend\"><% for (var i=0; i<datasets.length; i++){%><li><span style=\"background-color:<%=datasets[i].strokeColor%>\"></span><%if(datasets[i].label){%><%=datasets[i].label%><%}%></li><%}%></ul>',
        }
    }

    calibrateTemperature(event) {
        socket.emit("action", {module: "temperature", data: {current_temperature: this.calibration_value}})
    }

    temperatureChange(event) {
        this.calibration_value = event.target.value;
    }

    render() {
        return (
            <Segment>
                <Label className={"top attached"}>{this.props.name}</Label>
                <Input id="calibration_temperature" type="number" onChange={this.temperatureChange.bind(this)}/>
                <Button onClick={this.calibrateTemperature.bind(this)}>Set</Button>
                <div>
                    <Line
                        data={this.chartData()}
                        options={this.chartOptions()}
                    />
                </div>
            </Segment>
        );
    }
}

export default TemperatureGraph;
