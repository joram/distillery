
function updateValve(name){
  current = $("#"+name+"-current");
  target = $("#"+name+"-target");
  percent = $("#"+name+"-percent-bar");
  state = $("#"+name+"-status");
  form = $("#"+name+"-form");
	$.ajax({
		type: "GET",
		dataType: "json",
		url: "/api/valve/"+name,
		success: function(data){
      current.text(data.current);
      if(target.text() != data.target){
        target.text(data.target);
      }
      percent.css('width', data.current+'%').attr("aria-valuenow", data.current);
      state.text(data.status);
      checkMs = 50;
      if(data.status == "idle") { checkMs = 1000 };
      setTimeout(function(){
        updateValve(name);
      }, checkMs);
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
     dataType: "json",
    });
  }
  form.submit(changeValue);
}

