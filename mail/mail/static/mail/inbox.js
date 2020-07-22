document.addEventListener('DOMContentLoaded', function() {

	// Use buttons to toggle between views
	document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
	document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
	document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
	document.querySelector('#compose').addEventListener('click', compose_email);

	// By default, load the inbox
	load_mailbox('inbox');
});

function compose_email() {

	// Show compose view and hide other views
	document.querySelector('#emails-view').style.display = 'none';
	document.querySelector('#compose-view').style.display = 'block';

	const submitButton = document.getElementById('send-form');
	const subject = document.getElementById('compose-subject');
	const recipients = document.getElementById('compose-recipients');
	const body = document.getElementById('compose-body');

	// Clear out composition fields
	subject.value = '';
	body.value = '';
	recipients.value = '';

	// document.querySelector('#compose-recipients').value = '';
	// document.querySelector('#compose-subject').value = '';
	// document.querySelector('#compose-body').value = '';

	submitButton.disabled = true;
	recipients.addEventListener('keyup',()=>{
		console.log('test');
		if(recipients.value.length >0){
			submitButton.disabled = false;
		}
		else{
			submitButton.disabled = true;
		}
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
		}).then(result =>{
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
	
	// Show the mailbox and hide other views
	document.querySelector('#emails-view').style.display = 'block';
	document.querySelector('#compose-view').style.display = 'none';

	// Show the mailbox name
	document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
}

function catch_error(error){
	document.getElementById('error-view').innerHTML = `<h1> A problem occurred. </h1><p> ${error.message}</p>`
	show_view('view-error');
}

function show_view(id){
	document.querySelectorAll(`[id*="view-"]`).forEach((item)=> {
		item.style.display = (id === item.id ? 'block': 'none');
	})
	document.body.scrollTop;
}