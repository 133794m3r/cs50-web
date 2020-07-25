document.addEventListener('DOMContentLoaded', function() {
	document.querySelectorAll('.like').forEach( el=>{
		//each element calls the like function with it's id.
		el.addEventListener("click",()=>{like(el.id)});
	});
});


function like(element_id){
	const el = document.getElementById(element_id);
	console.log(el);
	let id = el.dataset.postid;
	fetch(`like/${id}`)
		.then(response => response.json())
		.then(result =>{
			el.className = (result.liked?'like liked':'like');
			document.getElementById(`likes-${id}`).innerText = result.likes;
		})
}

function follow_user(id){
	fetch(`follow/${id}`)
		.then(response=>response.json())
		.then(result=>{
			document.getElementById('follow').innerText = (result['followed']?'UnFollow':'Follow');
			document.getElementById('followers').innerText = result['followers'];
			document.getElementById('following').innerText = result['following'];
		})
}