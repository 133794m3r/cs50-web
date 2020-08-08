/**
 * CTFClub Project
 * Macarthur Inbody <admin-contact@transcendental.us>
 * Licensed under AGPLv3 Or Later (2020)
 */

/**
 *
 * The function below is a wrapper around fetch to make it work with POST requests when using Django.
 *
 * @param {string} route The URL that we're submitting to.
 * @param {object} content The parameters/variables that are to be included in the POST request.
 * @param {function(...[*]=)} callback A function to be called on the end of the fetch request.
 */
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

/**
 * This is just a wrapper around fetch for my get reqeusts to give me the json result.
 *
 * @param {string} route The URL we're submitting to.
 * @param {function(...[*]=)} callback The callback function to call upon the end of the fetch request.
 */
function get(route,callback){
	fetch(`${route}`)
		.then(response =>response.json())
		.then(result=>{
			callback(result)
		});
}

/**
 *
 * Gets a value from a cookie based upon the string name after exploding the cookie.
 * @param {string} name The name of the value we need to get.
 * @returns {null|string} The value of that property. Returns null if it isn't set.
 */
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