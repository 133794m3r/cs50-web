/**
 * When I created the code below only I and God knew what I was thinking.
 * Now only God knows. Be forewarned.
 */

/**
 * modal_challenge
 *
 * @param event {event} The event sent to it.
 * @param challenge_type {string} The challenge's short name.
 * @param edit {boolean} Whether this challenge already exists and should be an edit version.
 */
function modal_challenge(event,challenge_type,edit){
	event.preventDefault();
	let inner_content;
	let full_description = ''
	let flag = ''
	let chal = CHALLENGES[challenge_type];
	let challenge_name = chal.name;
	switch(challenge_type) {
		case "fizzbuzz":
		 //Code like the one below makes me thing I should've done it in react's JSX.
		 inner_content = `<div class="col-6">
			<div class="modal-input input-group mb-3">
				<div class="input-group-prepend">
					<label for="min" class="input-group-text">
					Min
					</label>
				</div>
				<input type="number" name="min" id="min" min="3" max="1200" class="input_items numbers"/>
			</div>
			<div class="modal-input input-group mb-3">
				<div class="input-group-prepend">
					<label for="max" class="input-group-text">
					Max
					</label>
				</div>
				<input type="number" name="max" id="max" min="1201" max="3000" class="input_items numbers"/>
			</div>
		</div>`;
		break;

		 default:
			flag = CHALLENGES[challenge_type].flag;
			let variety = 0;
			if ((challenge_type === 'hill' || challenge_type === 'affine')){
				challenge_name+=' - 0';
				let tmp = get_challenge_info(challenge_type,0);
				full_description = tmp.full_description;
				flag = tmp.flag;
				variety = tmp.variety;
				edit = tmp.edit;
			}
			document.getElementById('submit_chal').disabled = true;

			flag = flag ? flag : ''
			inner_content = `<div class="col-lg-7 col-md-8 col-sm-9 form-group">
				<textarea id='plain_text' name='plain_text' class="input_items form-text w-100" rows="2" cols="40" onkeyup="check_len('plain_text','submit_chal')">${flag}</textarea>
			</div>`;
			 if (challenge_type === 'hill' || challenge_type === 'affine') {
			 inner_content += `<div class="col-lg-5 col-md-4 col-sm-3 form-group">
					<select id="variety" onchange="change_variety()"><option value="0">Easy</option><option value="1">Medium</option></select>`;
			}
		 break;
	}


	const el = document.getElementById('input_description');
	if (edit === true) {
		const fd = document.getElementById('full_description');
		if(full_description == ''){
			full_description = chal.full_description;
		}
		 fd.innerHTML = `<p>For reference, the old challenge is below here.</p>`+full_description;
		 //+`<pre>Flag: ${flag}</pre>`;

		let el2 = document.getElementById('submit_chal');
		el2.disabled = false;
		el2.setAttribute('aria-disabled',"false");
		el2=document.getElementById('manage_challenge_hint');
		el2.hidden = false;
		el2.disabled = false;
		el2.setAttribute('aria-hidden',"false");
	}
	else{
		document.getElementById('full_description').innerHTML = ''

		let el2 = document.getElementById('submit_chal');
		el2.disabled = (challenge_type !== 'fizzbuzz');
		el2.setAttribute('aria-disabled',"true");
		el2=document.getElementById('manage_challenge_hint');
		el2.hidden = true;
		el2.disabled = true;
		el2.setAttribute('aria-hidden',"true");

	}
	el.innerHTML = `<span>${chal.description}</span>`;
	document.getElementById('challenge_modal_title').innerText = `${challenge_name}`; //-- Category:${chal.category}`;
	document.getElementById('input_row').innerHTML = inner_content;
	document.getElementById('sn').value = chal.sn;
	document.getElementById('editing').checked = (edit === true);
	$('#challenge_modal').modal('toggle');
}

function modal_hint(element,edit=true){
	const hint_id = element.dataset.id;
	console.log(element)
	document.getElementById('add_hint_modal').dataset.backdrop = 'static';
	document.getElementById('add_hint_modal_title').innerText = (hint_id != 0) ? "Edit Hint" : "Add Hint";
	document.getElementById("hint_challenge_name").value = element.dataset.cn;
	document.getElementById('submit_hint').innerText = (hint_id != 0) ? "Edit Hint" : "Add Hint";
	document.getElementById('submit_hint').disabled = (hint_id == 0)
	if(edit) {
		const hint_desc = document.getElementById(`${hint_id}-desc`).innerHTML;
		document.getElementById("hint_description").value = hint_desc;
		document.getElementById('hint_id').value = hint_id;
		document.getElementById('hint_level').value = element.dataset.lvl;
	}
	else{
		document.getElementById("hint_description").value = "";
	}
	$('#add_hint_modal').modal("toggle");

}

function check_len(input_id,button_id){
	const len = document.getElementById(input_id).value.length;
	document.getElementById(button_id).disabled = (len === 0 )
}

function submit_hint(){
	let hint_id = parseInt(document.getElementById("hint_id").value)
	const hint_level = parseInt(document.getElementById("hint_level").value);
	const hint_description = document.getElementById("hint_description").value;
	const challenge_name = document.getElementById("hint_challenge_name").value;
	if(hint_description.length === 0 || isNaN(hint_level) || challenge_name.length == 0 ){
		return;
	}
	hint_id = (isNaN(hint_id))?0:hint_id;

	let content = {};
	content['id'] = hint_id;
	content['challenge_name'] = challenge_name;
	content['description'] = hint_description;
	content['level'] = hint_level;

	submit(`/admin/challenge/hints/${challenge_name}/`,content,resp=>{
		if(hint_id == 0){
			content= `<tr><td id="${hint_id}-desc">${hint_description}</td><td><a href="#" data-id="${hint_id}" 
				data-lvl="${hint_level}" data-cn="${challenge_name}" class="edit_hint">Edit</a></td></tr>`;
			//Should do this with plain-ol javascript but oh well this works for now.
			$('#hints_body').append(content);
		}
		else{
			document.getElementById(`${hint_id}-desc`).innerHTML = hint_description;		
		}
	})
}

function submit_challenge(){
	let content = {}
	const sn = document.getElementById('sn').value;
	content['sn'] = sn;
	let chal = CHALLENGES[sn]
	content['name'] = chal.name;
	content['category'] = chal.category;
	let points = chal.points;

	if(chal.variety){
		content['variety'] = parseInt(document.getElementById('variety').value);
		document.getElementById('hint_modal_title').innerText = `${resp.hints.challenge_name} : Hints`
		//Points are adjusted based upon the variety value. Where the point bonus is basically 1+(0.33*(variety)). Also
		//I make sure that it's a nice even round number by making sure it ends in either a 5 or a zero.
		points = Math.ceil(chal.points *(1+(content['variety']/3)))
		points = points + (5 - (points % 5));
	}
	content['points'] = points;
	if(sn === 'fizzbuzz'){
		let min = parseInt(document.getElementById('min').value);
		let max = parseInt(document.getElementById('max').value);
		content['min'] = (min < 2 || min > 1200)?undefined:min
		content['max'] = (max < 1201 || max > 3000)?undefined:max
	}
	else{
		content['plaintext'] = document.getElementById('plain_text').value;
		if(content['plaintext'].length === 0 ){
			return;
		}
	}
	content['edit'] = document.getElementById('editing').checked;

	submit('/admin/challenge',content,response=>{
		//Eventually I'll actually use this data to update the local challenge data but that's not for now.
		// It's for a later thing. For now I just log the response. In the end I'll actually use the response to edit the
		// cached values.
		let variety = content['variety'] || -1;
		set_challenge_info(response,sn,variety);

	})
}


/**
 *
 * @param challenge_type {string} The shortname for the challenge aka it's functional shorthand.
 * @param variety {number} The variety.
 * @returns {object} Will return the object with the various fields I need to get.
 */
function get_challenge_info(challenge_type,variety=0){
	let tmp = {}
	let chal = {}
	for(let challenge in FULL_CHALLENGES){
		chal = FULL_CHALLENGES[challenge];
		if(chal.variety && chal.sn === challenge_type){
			//only call this if a variety is set and the shortname is the same as the one we're trying to get.
			if(chal.variety == variety) {
				tmp['full_description'] = chal.full_description;
				tmp['flag'] = chal.flag;
				tmp['variety'] = chal.variety;
				tmp['edit'] = chal.edit;
				return tmp;
			}
		}
	}
	return tmp
}

function set_challenge_info(new_info,challenge_type,variety = -1){
	let chal = {}
	for(let challenge in FULL_CHALLENGES){
		chal = FULL_CHALLENGES[challenge];
		if(chal.sn === challenge_type){

			chal.full_description = new_info.description;
			chal.flag = new_info.flag;
			if(variety === -1){
				chal.edit = true;
			}
			else if(variety !== -1){
				chal.edit = true;
				if(!chal.variety){
					chal.name = new_info.name;
					chal.variety = variety;
					FULL_CHALLENGES.push(chal);
					return;
				}
			}
			CHALLENGES[chal.sn].edit = true;
			FULL_CHALLENGES[challenge] = chal;
			return;
		}
	}
}

function fetch_challenge_hints(name,full=false){
	let challenge_name = name
	if(full === false) {
		if (CHALLENGES[name].variety) {
			challenge_name = `${CHALLENGES[name].name} - 0`
		}
		else{
			challenge_name = CHALLENGES[name].name;		
		}
	}
	else{
		challenge_name = CHALLENGES[name].name;
	}
	challenge_name = encodeURI(challenge_name);
	get(`/admin/challenge/hints/${challenge_name}/`,resp=>{
		console.log(resp);

		const len = resp.len;
		let content = ''
		if(len == 0){
			console.log(challenge_name);
			name = CHALLENGES[name].name;
			console.log(name)
			document.getElementById('hint_modal_title').innerText = `${name} : Hints`;

			document.getElementById('add_hint').dataset.cn = name;
			console.log(document.getElementById('add_hint'))
		}
		else if(len === 1){
			document.getElementById('add_hint').dataset.cn = resp.hints.challenge_name;
			content= `<tr><td id="${resp.hints.id}-desc">${resp.hints.description}</td><td><a href="#" data-id="${resp.hints.id}" 
				data-lvl="${resp.hints.level}" data-cn="${resp.hints.challenge_name}" class="edit_hint">Edit</a></td></tr>`;
		}
		else{
			document.getElementById('add_hint').dataset.cn = resp.hints[0].challenge_name;
			document.getElementById('hint_modal_title').innerText = `${resp.hints[0].challenge_name} : Hints`;
			let hints = resp.hints;
			for(let i=0;i<len;i++){
				content+= `<tr><td id="${resp.hints[i].id}-desc">${hints[i].description}</td><td><a href="#" data-id="${hints[i].id}"
					data-lvl="${resp.hints[i].level}" data-cn="${resp.hints[i].challenge_name}" class="edit_hint">Edit</a></td></tr>`;
			}
		}
		//document.getElementById('hints').innerHTML = content;
		document.getElementById('hints_body').innerHTML = content;
		document.querySelectorAll('.edit_hint').forEach(el=>{

			el.addEventListener("click",event=>{
				event.preventDefault();
				modal_hint(el);
			});
		})

		//document.getElementById('add_hint').dataset.cn = resp.hints.challenge_name;
		$('#hint_modal').modal("toggle");

	});
}

function change_variety(){
	let sn = document.getElementById('sn').value;
	let variety = document.getElementById('variety').value
	let title = document.getElementById('challenge_modal_title').innerText
	title = title.slice(0,-1);
	title = title + variety;
	document.getElementById('challenge_modal_title').innerText = title;
	let tmp = get_challenge_info(sn,variety);
	if(tmp.variety) {
		document.getElementById('editing').checked = true
		document.getElementById('full_description').innerHTML = `For reference, the old challenge is below here.<br /><br />${tmp.full_description}`;
		document.getElementById('plain_text').value = tmp.flag;

		let el = document.getElementById('submit_chal');
		el.disabled = false;
		el.setAttribute('aria-disabled',"false");
		el=document.getElementById('manage_challenge_hint');
		el.hidden = false;
		el.disabled = false;
		el.setAttribute('aria-hidden',"false");

	}
	else{
		document.getElementById('editing').checked = false;
		document.getElementById('full_description').innerHTML='';
		document.getElementById('plain_text').value = '';

		let el = document.getElementById('submit_chal');
		el.disabled = true;
		el.setAttribute('aria-disabled',"true");
		el = document.getElementById('manage_challenge_hint');
		el.disabled = true;
		el.hidden = true;
		el.setAttribute('aria-hidden',"true")

	}
}
