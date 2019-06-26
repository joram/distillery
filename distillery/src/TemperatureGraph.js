import React from 'react';
import {Label, Segment} from 'semantic-ui-react'
import {Line} from 'react-chartjs-2';

class TemperatureGraph extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            temperatureData: {},
        }
    }

    _create_graphjs_data(raw_data, metric_name) {
        let labels = [];
        let data = [];
        raw_data.forEach(datum => {
            if (datum.value === 0) {
                return
            }
            if (datum.value === 1024) {
                return
            }
            let t = new Date(datum.created * 1000);
            labels.push(t);
            data.push({
                t: t,
                y: datum.value,
            });
        });

        let graphjs_data = {
            labels: labels,
            datasets: [
                {
                    label: metric_name,
                    borderColor: 'rgba(75,192,192,1)',
                    data: data
                }
            ],

        };
        let graphjs_options = {
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
            annotation: {
                annotations: [{
                    type: 'line',
                    mode: 'horizontal',
                    scaleID: 'y-axis-0',
                    value: this.props.plant.min_moisture,
                    borderColor: 'rgb(192, 75, 75)',
                    borderWidth: 2,
                    label: {
                        enabled: false,
                        content: 'Min Moisture'
                    }
                }, {
                    type: 'line',
                    mode: 'horizontal',
                    scaleID: 'y-axis-0',
                    value: this.props.plant.max_moisture,
                    borderColor: 'rgb(75, 75, 192)',
                    borderWidth: 2,
                    label: {
                        enabled: false,
                        content: 'Max Moisture'
                    }
                }]
            }
        };
        return {
            data: graphjs_data,
            options: graphjs_options,
        }
    }

    render() {
        // let temperature_config = this._create_graphjs_data(this.state.temperatureData, "temperature");
        return (
            <Segment>
                <Label className={"top attached"}>{this.props.name}</Label>
                {/*<Line data={temperature_config.data} options={temperature_config.options} />*/}
                <Line data={{}}/>
            </Segment>
        );
    }
}

export default TemperatureGraph;
