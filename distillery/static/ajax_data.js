function ajax_onget(data){
  history = data['history']
  var data = new Array();
  $.each(history, function(key, val) {
    t = val['time']
    v = val['value']
    data.push([t,v])
  });
  return data
}

function get_data(){
  url = "http://192.168.1.4:5000/still/1/sensor/1?seconds_history=1000000"
  data = $.getJSON(url, ajax_onget);
  alert(data)
}

