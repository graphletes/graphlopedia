(function() {
	window.addEventListener("load", function() {	
		var def = document.getElementById('single');
		def.onclick = changeTab;
		def.click();
		document.getElementById('family').onclick = changeTab;
	});

	function changeTab(){
		var i, tabcontent, tablinks, target;

		tabcontent = document.getElementsByClassName("tabcontent");
	    for (i = 0; i < tabcontent.length; i++) {
	        tabcontent[i].style.display = "none";
	    }

	    tablinks = document.getElementsByClassName("tablinks");
	    for (i = 0; i < tablinks.length; i++) {
	        tablinks[i].className = tablinks[i].className.replace(" active", "");
	    }

	    target = this.id + "box"
	    document.getElementById(target).style.display = "block";
	    // document.getElementById(target).className += " active";
	    this.className += " active";
		}
})();