document.addEventListener('DOMContentLoaded', function() {
	document.querySelectorAll('.like').forEach( el=>{
		//each element calls the like function with it's id.
		el.addEventListener("click",like(el.dataset.id));
	});
});


function like(element_id){

}

function follow_user(id){
	fetch(`follow/${id}`)
		.then(response=>response.json())
		.then(result=>{

		})
}