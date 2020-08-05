function fetch_chal(challenge_id){
	get(`/challenge/${challenge_id}`,resp=>{
		document.getElementById('challenge_modal_title').innerText = resp.name;
		document.getElementById('description').innerHTML = resp.description;
		document.getElementById('points').innerText = `Points: ${resp.points}`;
		document.getElementById('challenge_id').value = resp.id;
		$('#challenge_modal').modal('toggle');
	})
}


function fetch_hint(hint_id){

}
function solve(event){
	event.preventDefault();
	const id = document.getElementById('challenge_id').value;
	const answer = document.getElementById('answer').value;
	submit(`/solve/${id}`,{'answer':answer},resp=>{
		console.log(resp);
	});
}