
	$(document).on("scroll", function(){
		if
      ($(document).scrollTop() > 60){
		  $("#banner").addClass("shrink");
		}
		else
		{
			$("#banner").removeClass("shrink");
		}
	});