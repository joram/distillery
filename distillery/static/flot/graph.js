var sensor_data = [[], [], []]
var sensor_names = ["boiler", 
					"outside", 
					"collection"]
var sensor_ids = [1, 2, 3]
var sensor_server_indices = [0, 0, 0]
var still_id = 1
var max_num_datums = 80
var options = { lines: {show: true},
			    points: {show: true},
				yaxis: {min: 10, max: 100},
			    xaxis: {tickDecimals: 0, tickSize: 1},
				legend:{        
                	noColumns: 0,
                	position: "nw"
            	}
		      };
var data_x = [0,0,0];
var poll_ms = 10000;
var sensor_poll_spacing = poll_ms/sensor_ids/length;

//var server = "192.168.1.4:5000"
//var server = "summer:5000"
var server = "96.50.21.187:5000"

function parse_sensor_data(series){
	still_id = series.still_id
	sensor_id = parseInt(series.sensor_id)
	sensor_index = sensor_ids.indexOf(sensor_id)
	num_datums = series.count

	for(var i=0; i<series.history.length; i++){
		id = parseInt(series.history[i].id)
		value = series.history[i].value
		time = data_x[sensor_index]++
	
		// add datum to list	
		sensor_data[sensor_index].push([time, value])
	
		// update max sesnor_id
		prev_max = sensor_server_indices[sensor_index]
		sensor_server_indices[sensor_index] = Math.max(prev_max, id)
	}

	si = sensor_index
	original_data = sensor_data[si]
	if(sensor_data[si].length > max_num_datums){
		start_index = sensor_data[si].length-max_num_datums
		end_index = sensor_data[si].length
		sensor_data[si] = sensor_data[si].slice(start_index, end_index)
	}

	final_data = []
	for(var i=0; i<sensor_ids.length; i++){
		last_datum = sensor_data[i][sensor_data[i].length-1];
		last_val = "unknown"
		if(last_datum){
			last_val = last_datum[1].toFixed(2);
		}
		//last_val = "";
		final_data.push({label: sensor_names[i]+" ("+last_val+")", 
						 data: sensor_data[i]})
	}

	$.plot("#placeholder", final_data, options);
	update_y_axis_bounds();
	return sensor_id
}


function updateData(sensor_id){
	sensor_index = sensor_ids.indexOf(sensor_id)
	lki = sensor_server_indices[sensor_index]
	
	function receiveUpdateData(series){
		sensor_id = parse_sensor_data(series)
		setTimeout( updateData, poll_ms, sensor_id)
	}
	
	$.ajax({
		url: "http://"+server+"/still/"+still_id+"/sensor/"+sensor_id+"?last_known_index="+lki+"",
		type: "GET",
		dataType: "json",
		success: receiveUpdateData
	});
}

function init_graph() {

	function receiveInitData(series){
		series.history = series.history.reverse()
		sensor_id = parse_sensor_data(series)
		setTimeout( updateData, poll_ms, sensor_id)
	}
	
	function requestInitData(sensor_id){
		$.ajax({
			url: "http://"+server+"/still/"+still_id+"/sensor/"+sensor_id+"?previous_count="+max_num_datums+"",
			type: "GET",
			dataType: "json",
			success: receiveInitData
		});
		
	}

	for(var i=0; i<sensor_ids.length; i++){
		sensor_id = sensor_ids[i]
		delay = sensor_poll_spacing*i;
		setTimeout(requestInitData, delay, sensor_id)
	}
}

function update_y_axis_bounds(){
	var max = 0, min = 0, padding = 5;
	_.each(final_data, function (e, i) {
		if (e.data) {
			
			var _max = _.max(e.data, function (dataEl) {
				if (dataEl && dataEl[1]) {
					return dataEl[1];
				}
			});
	
			var _min = _.min(e.data, function (dataEl) {
				if (dataEl && dataEl[1]) {
					return dataEl[1];
				}
			});
	
			if (_max[1] > max) {
				max = _max[1];
			}
	
			if (_min[1] < min) {
				min = _min[1];
			}
		}
	});
	
	max = max + padding;
	min = min - padding;
	options.yaxis = {min: min, max: max};
}
