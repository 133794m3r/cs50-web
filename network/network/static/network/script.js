document.addEventListener('DOMContentLoaded', function() {
	document.querySelectorAll('.like').forEach( el=>{
		//each element calls the like function with it's id.
		el.addEventListener("click",like(el.dataset.id));
	});
});


function like(element_id){

}