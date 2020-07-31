function submit(route,content,callback){
	const csrftoken = cookie_value('csrftoken');
	fetch(route,{
		method:"POST",
		headers:{
			'Content-Type':'application/json',
			'X-CSRFToken':csrftoken,
			'X-Requested-With':'XMLHttpRequest'
		},
		credentials:"same-origin",
		body:JSON.stringify(content)
	})
		.then(response=>response.json())
		.then(result=>{
			if(callback){
				callback(result)
			}
		});
}

function get(route,callback){
	fetch(`${route}`)
		.then(response =>response.json())
		.then(result=>{
			callback(result)
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