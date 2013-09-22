

function initialize_graph() {
	var options = { lines: {show: true},
				points: {show: true},
				xaxis: {tickDecimals: 0,
						tickSize: 1}
			  };
	var sensor_1_data = []
	var sensor_2_data = []
	var sensor_3_data = []
	var data = []
	$.plot("#placeholder", data, options);

	$("button.dataUpdate").click(
		getAllSensors()
	);
	
	function getAllSensors(){

		var data_x = [0,0,0];
		function getAllSensorData(){
			function getSensor(still_id, sensor_id){
				function onDataReceived(series) {
					
					// create a list of all new data
					var new_data = []
					for(var i=0; i<series.history.length; i++){
						new_data.push([data_x[sensor_id]++, series.history[i].value])
					}

					// add new data to existing list
					if(sensor_id == 1){ sensor_1_data = sensor_1_data.concat(new_data) }
					if(sensor_id == 2){ sensor_2_data = sensor_2_data.concat(new_data) }
					if(sensor_id == 3){ sensor_3_data = sensor_3_data.concat(new_data) }
					
					// maintain max length of data
					var max_length = 100
					if(sensor_1_data.length > max_length){
						sensor_1_data = sensor_1_data.splice(0,sensor_1_data.length-max_length)
					}
					if(sensor_2_data.length > max_length){
						sensor_2_data = sensor_2_data.splice(0,sensor_2_data.length-max_length)
					}
					if(sensor_3_data.length > max_length){
						sensor_3_data = sensor_3_data.splice(0,sensor_3_data.length-max_length)
					}

					data = [sensor_1_data, sensor_2_data, sensor_3_data]
					$.plot("#placeholder", data, options);
				}

				// get data, pass to onDataReceived
				$.ajax({
					url: "http://summer:5000/still/"+still_id+"/sensor/"+sensor_id+"?seconds_history=1000000",
					type: "GET",
					dataType: "json",
					success: onDataReceived
				});
			}

			getSensor(1, 1);
			getSensor(1, 2);
			getSensor(1, 3);
			setTimeout(getAllSensorData, 10000);
		}
		getAllSensorData();
	}
}
