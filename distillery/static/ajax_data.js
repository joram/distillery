function parse_json(data){
  history = data['history']
  var data = new Array();
  $.each(history, function(key, val) {
    t = val['time']
    v = val['value']
    data.push([t,v])
  });

  alert("A "+data.length)
  debug_show_data(data);
  return data
}

function debug_show_data(data){
  var body = document.getElementsByTagName('body')[0]

  alert("B "+data.length);  
  for (var i = 0; i < data.length; i++) {
    var time = data[i][0];
    var value = data[i][1];

    if (value != 0){
      var div = document.createElement("div");
      div.innerHTML = time + " - " + value;
      body.appendChild(div);
    }
  }
}

function ajax_in_new_data(){
  url = "http://192.168.1.4:5000/still/1/sensor/1?seconds_history=1000000"
  data = $.getJSON(url, parse_json);
}

