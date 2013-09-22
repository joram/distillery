
function json_callback(error, json_data){
  if (error){ alert("received error"); }
  
  // build data array
  history = json_data['history']
  var data = [];
  var minObjectValue;
  var maxObjectValue;
  $.each(history, function(key, val) {
    
    // build datum
    datum = {};
    date_str = val['time'];
    datum.date = key; //Date.parse(date_str);
    datum.value = val['value'];
    if(datum.value > 0){
      data.push(datum);

      // note max and mins
      if(typeof minObjectValue === "undefined"){ minObjectValue = datum.value; }
      if(typeof maxObjectValue === "undefined"){ maxObjectValue = datum.value; }
      if(minObjectValue > datum.value){ minObjectValue = datum.value; }
      if(maxObjectValue < datum.value){ maxObjectValue = datum.value; }
    }
  });

  // these are graph size settings
  var width = 1500, height = 800;
  var margin = {top: 30, right: 10, bottom: 40, left: 60};
  var width = width - margin.left - margin.right;
  var height = height - margin.top - margin.bottom;
 
  var minDate = (data[0].date);
  var maxDate = data[data.length-1].date;
//  minObjectValue = getMinObjectValue(data, 'value');
//  maxObjectValue = getMaxObjectValue(data, 'value');
//  maxObjectValue = 0.04;
 
  //remove the old graph object
  $('svg').remove();


  //create the graph object
  var vis= d3.select("#graph").append("svg")
   .data(data)
   .attr("class", "metrics-container")
   .attr("width", width + margin.left + margin.right)
   .attr("height", height + margin.top + margin.bottom)
   .append("g")
   .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
 
  //var y = d3.scale.linear().domain([ minObjectValue - (.1 * minObjectValue) , maxObjectValue + (.1 * maxObjectValue) ]).range([height, 0])
  var y = d3.scale.linear().domain([minObjectValue, maxObjectValue]).range([height, 0])
  var x = d3.time.scale().domain([minDate, maxDate]).range([0, width]);
 
  var yAxis = d3.svg.axis()
   .scale(y)
   .orient("left")
   .ticks(5);
 
  var xAxis = d3.svg.axis()
   .scale(x)
   .orient("bottom")
   .ticks(5);
 
  vis.append("g")
   .attr("class", "axis")
   .call(yAxis);
 
  vis.append("g")
   .attr("class", "axis")
   .attr("transform", "translate(0," + height + ")")
   .call(xAxis);
 
	//add the axes labels
	vis.append("text")
	    .attr("class", "axis-label")
	    .attr("text-anchor", "end")
	    .attr("x", 20)
	    .attr("y", height + 34)
	    .text('Date');
 
	vis.append("text")
	    .attr("class", "axis-label")
	    .attr("text-anchor", "end")
	    .attr("y", 6)
	    .attr("dy", "-4em")
	    .attr("transform", "rotate(-90)")
	    .text('Temperature in C');
 
	var line = d3.svg.line()
		.x(function(d) { return x(d["date"]); })
		.y(function(d) { return y(d["value"]); })
 
	vis.append("svg:path")
		.attr("d", line(data))
		.style("stroke", function() { 
			return "#000000";
		})
		.style("fill", "none")
		.style("stroke-width", "2.5");
 
		var dataCirclesGroup = vis.append('svg:g');
 
		var circles = dataCirclesGroup.selectAll('.data-point')
			.data(data);
 
		circles
			.enter()
			.append('svg:circle')
			.attr('class', 'dot')
			.attr('fill', function() { return "red"; })
			.attr('cx', function(d) { return x(d["date"]); })
			.attr('cy', function(d) { return y(d["value"]); })
			.attr('r', function() { return 3; })
			.on("mouseover", function(d) {
  				d3.select(this)
					.attr("r", 8)
					.attr("class", "dot-selected")
					.transition()
      					.duration(750);
			})
			.on("mouseout", function(d) {
  				d3.select(this)
					.attr("r", 3)
					.attr("class", "dot")
					.transition()
      					.duration(750);
			});
 
}


function update_data(){
  url = "http://192.168.1.4:5000/still/1/sensor/1?seconds_history=1000000"
  d3.json(url, json_callback)
}

