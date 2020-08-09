document.addEventListener('DOMContentLoaded', function() {
	document.querySelectorAll('.like').forEach( el=>{
		//each element calls the like function with it's id.
		el.addEventListener("click",event=>{like(event,el.id)});
	});
	document.querySelectorAll('.edit_link').forEach(el=>{
		el.addEventListener("click",event=>{
			edit_post(event,el.dataset.postid);
		})
	})
	let el = document.getElementById('edit_form');
	if(el !== null) {
		document.getElementById('edit_form').addEventListener('submit', event => {
			submit_edit(event)
		});
	}
});


function like(event,element_id){
	event.preventDefault();
	const el = document.getElementById(element_id);
	let id = el.dataset.postid;
	fetch(`/like/${id}`)
		.then(response => response.json())
		.then(result =>{
			el.className = (result.liked?'like liked':'like');
			document.getElementById(`likes-${id}`).innerText = result['likes'];
		})
		.catch(error=>{
			console.log("Error:",error);
		});		
}
//This will be called when they click the "edit post" link and will prevent it from redirecting if they have JS but if they don't
//we'll take them to the "edit" view. Othewrise we'll simply get the post and replace the contents of new post with that data.
function edit_post(event,id){
	event.preventDefault();
	document.getElementById('new_post').style.display = 'none';
	const content = document.getElementById(`post_content_${id}`).innerText
	document.getElementById('edit_post').style.display = 'block';
	let el = document.getElementById('edit_content');
	el.innerText = content;
	el.dataset.postid = id;
}

function follow_user(id){
	const csrftoken = cookie_value('csrftoken');
	fetch(`/follow/${id}`,{
		method:'POST',
		headers:{
		'Content-Type':'application/json',
			'X-CSRFToken':csrftoken,
			'X-Requested-With':'XMLHttpRequest'
		},
		credentials:"same-origin"
	})
		.then(response=>response.json())
		.then(result=>{
			document.getElementById('follow').innerText = (result['followed']?'UnFollow':'Follow');
			document.getElementById('followers').innerText = result['followers'];
			document.getElementById('following').innerText = result['following'];
		})
		.catch(error=>{
			console.log("Error:",error);
		});
}

function cookie_value(name){
	let value = null;
	if(document.cookie && document.cookie !== ''){
		const cookies = document.cookie.split(';');
		let cookie = '';
		for(let i=0;i<cookies.length;i++){
			cookie = cookies[i].trim();
			if(cookie.startsWith(`${name}=`)){
				value = decodeURIComponent(cookie.substring(name.length+1));
				break;
			}
		}
	}
	return value;
}

function submit_edit(event){
	event.preventDefault();
	const el = document.getElementById('edit_content');
	const id=el.dataset.postid;
	const content = el.value;
	console.log(content);
	const csrftoken = cookie_value('csrftoken');
	fetch(`/edit/post/${id}`,{
		method:"POST",
		headers:{
			'Content-Type':'application/json',
			'X-CSRFToken':csrftoken,
			'X-Requested-With':'XMLHttpRequest'
		},
		credentials:"same-origin",
		body:JSON.stringify({content:content})
	})
		.then(response=>response.json())
		.then(result=>{
			console.log(result);
			document.getElementById(`post_content_${id}`).innerText = result.post;
			document.getElementById('new_post').style.display = 'block';
			document.getElementById('edit_post').style.display = 'none';
		})
		.catch(error=>{
			console.log("Error:",error);
		});
}
