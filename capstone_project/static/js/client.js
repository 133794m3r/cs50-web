/**
 * CTFClub Project
 * Macarthur Inbody <admin-contact@transcendental.us>
 * Licensed under AGPLv3 Or Later (2020)
 */

function fetch_chal(challenge_id){
	get(`/challenge/${challenge_id}`,resp=>{
		console.log(resp);
		const solved = resp.solved;
		const challenge = resp.challenge;
		const num_hints = resp.num_hints;
		const hints = resp.hints;
		document.getElementById('challenge_modal_title').innerText = challenge.name;
		document.getElementById('description').innerHTML = challenge.description;
		document.getElementById('points').innerText = `Points: ${challenge.points}`;
		document.getElementById('challenge_id').value = challenge.id;
		let hint_html = ''
		if(num_hints === 1) {
			hint_html += `<div class="col-12 text-center mb-2">
								<button class="btn btn-info hints" data-id="${hints.id}">
								<span>View Hint Level ${hints.level}</span></button>
							</div>`
		}
		else if(num_hints > 1){
			for (let i = 0; i < num_hints; i++) {
				hint_html += `<div class="col-12 text-center mb-2">
								<button class="btn btn-info hints" data-id="${hints[i].id}">
								<span>View Hint Level ${hints[i].level}</span></button>
							</div>`
			}
		}

		document.getElementById('hints_container').innerHTML = hint_html;

		const answer_el = document.getElementById('answer');
		if(solved){
			answer_el.value = challenge.flag;
			answer_el.setAttribute('readonly','true');
		}
		else{
			answer_el.removeAttribute('readonly');
			answer_el.value = '';
		}

		document.querySelectorAll('.hints').forEach(el=>{
			el.addEventListener('click',event=>{
				fetch_hint(el.dataset.id);
			});
		});
		$('#challenge_modal').modal('toggle');
	})
}


function fetch_hint(hint_id){
	get(`/hint/${hint_id}`,resp=>{
		document.getElementById('hint_body').innerHTML = resp.description;
		$('#hint_modal').modal('toggle');
	});
}

function dismiss_alert(){

}
function solve(event){
	event.preventDefault();
	const id = document.getElementById('challenge_id').value;
	const answer = document.getElementById('answer').value;
	submit(`/solve/${id}`,{'answer':answer},resp=>{
		console.log(resp);
		let msg = ''
		let type = ''
		if(resp.solved){
			msg = "Solved!";
			type = 'alert-success';
		}
		else{
			msg = "Wrong Answer";
			type = 'alert-danger';
		}
		let alert = `<div class="alert ${type} alert-dismissible fade show" role="alert"> ${msg}</div>`
		document.getElementById('alert_msg').innerHTML = alert;

		document.getElementById('challenge_body').scrollTop += 100
		window.setTimeout((old_top)=>{
				$('.alert').alert('close');
				document.getElementById('challenge_body').scrollTop += 100
				//window.scrollTop = old_top;
		},3000);
	});
}

function score_password(button_el,username,password,password_confirm_id){
	let inputs=new Array(3)

	//We're going to include their username in the ZXCVBN password strength estimator.
	inputs[0]=(username != '')?document.getElementById(username).value:'';
	//Plus if their username is uppercase as the first letter.
	inputs[1]= inputs[0] === ''?"":inputs[0].substr(0,1).toUpperCase()+inputs[0].substr(1);
	//also include the name of the URl that this is used on.
	inputs[2]=location.hostname;
	password=document.getElementById(password).value;

	let el=document.getElementById('score');
	if(password !== document.getElementById(password_confirm_id).value){
		 el.innerText="Passwords must Match!";
			el.setAttribute("style","color:red;font-weight:bold");
		 return;
	}
	let result=zxcvbn(password,inputs);
	let guesses = result.guesses_log10;
	let score;
	if(guesses <= 5.6){
		score = 0;
	}
	else if(guesses <= 5.7){
		score = 1;
	}
	else if(guesses <= 7.8){
		score = 2;
	}
	else if(guesses <= 8){
		score = 3;
	}
	else if(guesses <= 9){
		score = 4;
	}
	else if(guesses <= 9.9){
		score = 5;
	}
	else{
		score = 6;
	}
	console.log(score);
	switch(score){
		case 0:
			el.innerText="Unusable Password";
			el.setAttribute('style','color:red; font-weight:bold;')
			break;
		case 1:
			el.innerText="Unsafe Password";
			el.setAttribute('style','color:#FF2400; font-weight:bold;')
			break;
		case 2:
			el.innerText="Extremely Weak Password";
			el.setAttribute('style','color:#FF7900; font-weight:bold;')
			break;
		case 3:
			el.innerText="Barely Acceptable Password";
			el.setAttribute('style','color:orange; font-weight:bold;')
			break;
		case 4:
			el.innerText="Somewhat-Safe Password";
			el.setAttribute('style','color:yellow;font-weight:bold;');
			break;
		case 5:
			el.innerText="Safe Password";
			el.setAttribute('style','color:yellowgreen; font-weight:bold;')
			break;
		default:
			el.innerText="Extremely Safe Password";
			el.setAttribute('style','color:green; font-weight:bold;')
			break;
	}

	if(score <= 3){
		let feedback=(result.feedback.warning !== '')?result.feedback.warning+'. ':' Also think about adding numbers.';
		feedback+=result.feedback.suggestions.join(' ');
		document.getElementById('password_feedback').innerText=feedback;
	}
	else{
		document.getElementById('password_feedback').innerText = '';
	}

	let but = document.getElementById(button_el)
	if (score < 3) {
		but.setAttribute('aria-disabled', "true");
	}
	else {
		but.setAttribute('aria-disabled', "false");
	}

	but.disabled = (result.score < 3);

	return result.score;
}