var datasetColors;
var lastDt;
var chart;
var options = {
	responsive: true,
	maintainAspectRatio: false,
	scales: {
		xAxes: [{
			type: 'time',
			time: {
				unit: 'minute',
				displayFormats: {
					millisecond: "mm:ssA",
					second: "mm:ssA",
					minute: "mm:ssA",
				}
			}
		}]	
	}
};


function initGraph(chartId){
	datasetColors = randomColor({count: 8, hue:"red", format:"rgba"});
	chartCtx = $("#"+chartId);
	chart = new Chart(chartCtx, {
		type: 'line',
		data:  {
			datasets: [],
			labels: [],
		},
		options: options,
	});
	updateGraph();
	setInterval(updateGraph, 2000);
}


function updateGraph(){
	$.ajax({
		type: "GET",
		data: {
			"dt": lastDt,
		},
		dataType: "json",
		url: "/api/temperatures",
		success: updateGraphData,
	});
}


function updateGraphData(data){
	probeIndex = 0;
	Object.keys(data).forEach(function(probeName){

		// init new datasets
		if(chart.data.datasets.length <= probeIndex){
			dataset = {
				label: probeName,
				data: [],
				borderColor: datasetColors[probeIndex],
				backgroundColor: datasetColors[probeIndex],
				fill: false,
			};
			chart.data.datasets.push(dataset);
		}

		// add new data	
		dataset = chart.data.datasets[probeIndex];
		addData(data[probeName], dataset, probeIndex==0);
		trimData(dataset, probeIndex==0);
		probeIndex += 1;
	});
	chart.update();
}


function addData(data, dataset, addLabels){
	data.forEach(function(datum){
		dt = new Date(datum["t"]);
		newDatum = {
			t: dt,
			y: datum["y"],
		};

		datumExists = false;
		dataset.data.forEach(function(existingDatum){
			if(existingDatum.t.getTime() == dt.getTime()){
				datumExists = true;
			};
		});

		if(!datumExists){
			dataset.data.push(newDatum);
			if(addLabels){
				chart.data.labels.push(dt);
			}
    }
	});
}

function trimData(dataset, trimLabels){
  maxDuration = moment.duration(30, "minutes"); 
  now = moment($.now());
	earliest = now-maxDuration;

	dataset.data = dataset.data.filter(function( datum ) {
	  t = moment(datum.t.getTime());
		return t > earliest;
  });

	if(trimLabels){
	  chart.data.labels = chart.data.labels.filter(function( label ) {
		  return label > earliest;
		});
	}
}
