function fetch_chal(challenge_id){
	get(`/challenge/${challenge_id}`,resp=>{
		console.log(resp);
	})
}