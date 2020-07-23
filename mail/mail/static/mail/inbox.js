let current_mailbox = '';
document.addEventListener('DOMContentLoaded', function() {

	// Use buttons to toggle between views
	document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
	document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
	document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
	document.querySelector('#compose').addEventListener('click', compose_email);
    document.querySelector('#read-archive').addEventListener('click', function(){
    	const archived_flag = (this.dataset.archived == 'false'?true:false);
    	//always go back to the current mailbox.
        toggle_archive(this.dataset.email, {archived:archived_flag});
	});

	// By default, load the inbox
	load_mailbox('inbox');
});

function compose_email() {

	// Show compose view and hide other views
	show_view('compose-view');
	const submitButton = document.getElementById('send-form');
	const subject = document.getElementById('compose-subject');
	const recipients = document.getElementById('compose-recipients');
	const body = document.getElementById('compose-body');

	// Clear out composition fields
	subject.value = '';
	body.value = '';
	recipients.value = '';


	submitButton.disabled = true;
	recipients.addEventListener('keyup',()=>{

		submitButton.disabled = recipients.value.length <= 0;
	})

	document.getElementById('compose-form').onsubmit = () =>{
		fetch('/emails',{
			method: 'POST',
			body:JSON.stringify({
				recipients:recipients.value,
				subject:subject.value,
				body:body.value,
				read: false
			})
		}).then(response=>response.json()).then(result =>{
			if(result.error){
				document.getElementById('recipients-error').textContent = result.error
				recipients.className = 'form-control is-invalid'
			}
			else {
				load_mailbox('sent');
			}
		}).catch(error =>{
			catch_error(error);
		})

		return false;
	}
}

function load_mailbox(mailbox) {
	current_mailbox = mailbox;
	// Show the mailbox and hide other views
	document.querySelector('#emails-view').style.display = 'block';
	document.querySelector('#compose-view').style.display = 'none';

	// Show the mailbox name
	document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
	fetch(`/emails/${mailbox}`).then(response=>{
		if(!response.ok){
			throw Error(response.status + '-' + response.statusText);
		}
		return response.json()
	}).then(emails =>{
		const el = document.getElementById('emails-view');
		el.innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.substr(1)}</h3>`
		show_view('emails-view');
		if(emails.length === 0){
			el.innerHTML += '<h3> You have no Emails.</h3>';
		}
		else{
			emails.forEach(email=>{
				const email_item = document.createElement('div');
				email_item.addEventListener('click',()=>{
					read_email(email.id,(mailbox === 'sent'));
				});
				email_item.className = 'list-group-item list-group-item-action ';
				email_item.className += (email.read?'list-group-item-secondary':'')
				email_item.href = '#';
				let content = (mailbox !== 'sent'?`<div class="col-sm"><b>From</b>  ${email.sender} </div>`:'');
				content+=(mailbox !== 'inbox'?`<div class="col-sm"><b>To:</b> ${email.recipients} </div>`:'');
				content+='<div class="col-sm"><b> Subject:</b> '+(email.subject?email.subject:'(No Subject)')+'</div>';
				content+=`<span class="badge badge-info badge-pill">${email.timestamp}</span>`;
				content=`<div class="container"><div class="row">${content}</div></div>`
				email_item.innerHTML = content;
				el.append(email_item);
			});
		}
	})
}

function fetch_email(id,callback){
		fetch(`/emails/${id}`)
		.then(response=>{
			if(!response.ok){
				throw Error(response.status + '-' + response.statusText);
			}
			return response.json();
		}).then(email=>{
			return callback(email);
		})
}

function read_email(id,sent = false){
	fetch_email(id,email=> {
		const email_fields = ['sender', 'recipients', 'timestamp', 'subject', 'body'];
		email_fields.forEach(key => {
			document.getElementById(key).innerText =
				(email[key] ? email[key] : '(No ' + key.charAt(0).toUpperCase() + key.substr(1) + ')');
		});
		document.querySelectorAll(`[id*="read-"]`).forEach(item => {
			item.dataset.email = email.id;
			if (item.id === 'read-archive') {
				if (sent) {
					item.style.display = 'none';
				}
				else {
					item.textContent = (email.archived ? 'Un-Archive' : 'Archive');
					item.dataset.archived = email.archived;
					item.style.display = 'block';
				}
			}
		});
		if (!email.read) {
			update_flags(email.id, {'read': true});
		}
		document.getElementById('read-reply').addEventListener('click',()=>{
			reply_email(email)
		});
	});

	show_view('read-view');
}

function catch_error(error){
	document.getElementById('error-view').innerHTML = `<h1> A problem occurred. </h1><p> ${error.message}</p>`
	show_view('view-error');
}

function reply_email(email){
	let subj = email.subject;
	if(!(subj.match(/^R[Ee]:/))){
		subj = `RE: ${subj}`;
	}
	let body = '> '+email.body
	let sender = (current_mailbox == 'sent'?email.recipients:email.sender);
	//make sure that it confirms to the standard of email clients by prepending each line with a > followed by a space.
	email.body.replace(/\r?\n/g,`$&>`);
	body = `\nOn ${email.timestamp} ${email.sender} wrote:\n${body}`
	compose_email();
	document.getElementById('compose-recipients').value = sender;
	document.getElementById('compose-subject').value = subj;
	document.getElementById('compose-body').value = body;
	document.getElementById('send-form').disabled = false;
}

function show_view(id){
	document.querySelectorAll(`[id*="-view"]`).forEach((item)=> {
		item.style.display = (id === item.id ? 'block': 'none');
	})
	document.body.scrollTop;
}

function toggle_archive(email_id,flags){
	update_flags(email_id,flags,load=>{
		load_mailbox(current_mailbox);
	})
}

function update_flags(email_id,flags={},callback){
	if(flags === {}){
		return false;
	}

	fetch(`/emails/${email_id}`,{
		method:'PUT',
		body:JSON.stringify(flags)
	}).then(response=>{
		if(!response.ok){
			throw Error(response.status+'-'+response.statusText);
		}
		if(callback){
			callback()
		}
		return true;
	}).catch(error=>{
		catch_error(error);
	})
}