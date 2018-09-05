
function updateValve(name){
  current = $("#"+name+"-current");
  target = $("#"+name+"-target");
  state = $("#"+name+"-status");
  form = $("#"+name+"-form");

	$.ajax({
		type: "GET",
		dataType: "json",
		url: "/api/valve/"+name,
		success: function(data){
      current.text(data.current);
      target.text(data.target);
      state.text(data.status);
      if(data.status != "idle") {
        setTimeout(function(){
          updateValve(name)
        }, 500)
      }
    },
	});
}

function setupValve(name){
  updateValve(name);
  current = $("#"+name+"-current");
  target = $("#"+name+"-target");
  state = $("#"+name+"-status");
  form = $("#"+name+"-form");

  function changeValue(event){
    event.preventDefault();
    targetVal = target.val();
    console.log("posting form. target:"+targetVal);
    $.ajax({
     type: "POST",
     url: "/api/valve/"+name,
     data: {"target": targetVal},
     success: function(data){
       console.log("success");
       updateValve(name);
     },
     dataType: "json",
    });
  }
  form.submit(changeValue);
}

