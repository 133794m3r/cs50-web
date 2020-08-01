function modal_challenge(event,challenge_type,edit){
	event.preventDefault();
	let inner_content;
	let full_description = ''
	let flag = ''
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
			if ((challenge_type === 'hill' || challenge_type === 'affine') && edit){
				let tmp = get_challenge_info(challenge_type,0);
				full_description = tmp.full_description;
				flag = tmp.flag;
				variety = tmp.variety;
				edit = 'true';
			}
			document.getElementById('submit_chal').disabled = true;
			flag = flag ? flag : ''
			inner_content = `<div class="col-6 form-group">
				<textarea id='plain_text' name='plain_text' class="input_items form-text" rows="3" cols="40" onkeyup="check_len()">${flag}</textarea>
			</div>`;
			 if (challenge_type === 'hill' || challenge_type === 'affine') {
			 inner_content += `<div class="col-6 form-group">
					<select id="variety" onchange="change_variety()"><option value="0">Easy</option><option value="1">Hard</option></select>`;
			}
		 break;
	}
	let chal = CHALLENGES[challenge_type];
	const el = document.getElementById('input_description');
	if (edit === 'true') {
		const fd = document.getElementById('full_description');
		if(full_description == ''){
			full_description = chal.full_description;
		}
		 fd.innerHTML = `<p>For reference, the old challenge is below here.</p>`+full_description+
			 `<pre>Flag: ${flag}</pre>`;
	}
	// else{
	el.innerHTML = `<span>${chal.description}</span>`;
	// }
	document.getElementById('challenge_modal_title').innerText = `${chal.name} -- Category:${chal.category}`;
	document.getElementById('input_row').innerHTML = inner_content;
	document.getElementById('sn').value = chal.sn;
	document.getElementById('editing').checked = (edit === 'true');
	$('#challenge_modal').modal('toggle');
}


function check_len(){
	const len = document.getElementById('plain_text').value.length;
	document.getElementById('submit_chal').disabled = (len === 0 )
}


function submit_challenge(){
	let content = {}
	const sn = document.getElementById('sn').value;
	content['sn'] = sn;
	content['name'] = CHALLENGES[sn].name;
	content['category'] = CHALLENGES[sn].category;
	if(sn === 'affine' || sn === 'hill'){
		content['variety'] = parseInt(document.getElementById('variety').value);
	}
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
	console.log(content)
	submit('/challenge_admin',content,response=>{
		//Eventually I'll actually use this data to update the local challenge data but that's not for now.
		// It's for a later thing. For now I just log the response. In the end I'll actually use the response to edit the
		// cached values.
		console.log(response)
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

function change_variety(){
	let sn = document.getElementById('sn').value;
	let variety = document.getElementById('variety').value
	let tmp = get_challenge_info(sn,variety);
	if(tmp.variety) {
		document.getElementById('editing').checked = true
		document.getElementById('full_description').innerHTML = tmp.full_description;
		document.getElementById('plain_text').value = tmp.flag;
	}
	else{
		document.getElementById('editing').checked = false;
		document.getElementById('full_description').innerHTML='';
		document.getElementById('plain_text').value = ''
	}
}