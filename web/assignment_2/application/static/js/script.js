//

Array.prototype.removeItem=function(needle){
	let index = this.indexOf(needle)
	if(index > -1){
		return this.splice(index,1);
	}
}

Date.prototype.toLocalTime=function() {
	return this.toLocaleString('en-us', {timeZone: 'America/New_York'})
}

//the globals
var g_channels = [];
var g_users = [];
var g_current_channel = "";
var g_private = {'names':[],'passwords':[]};
var g_username = localStorage.getItem('username')
var socket;
var g_private = false;
$('body').ready(()=>{

	socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

	if (!g_username){
		$('#main_modal').modal('toggle');
		$('#modal_input').data('type','username');
	}
	else{
		add_user(g_username)
		socket.emit('rejoin',{'username':g_username});
	}

	window.onbeforeunload = function () {
		socket.emit('client_disconnect', {'username':localStorage.getItem('username')});
	}

	$("#modal_input").on('keyup', function (key) {
		if (document.getElementById('modal_input').value.length > 0) {
			$("#modal_button").attr('disabled', false);

			if (key.keyCode === 13) {
				$('#modal_button').click();
			}
		}
		else {
			$("#modal_button").attr('disabled', true);
		}
	});


	$('#modal_button').on('click',()=>{
		let input=$("#modal_input");
		let input_val=input.val();
		switch(input){
			case "username":
				//let username=input.val();
				if(input_val in g_users){
					$('#main_modal_title').text('This user already exists. Please select another.');
				}
				else {
					socket.emit('new_user', {'username': input_val});
				}
				break;

			case "channel":
				//let name=input.val();
				if(input_val in g_channels || input_val in g_private){
					$('#main_modal_title').text('This channel already exists. Please select another name.');
				}
				else {
					socket.emit('new_channel',{'channel':input_val});
				}
				break;

			case "private_channel":
				//let name=input.val();
				if(input_val in g_channels || input_val in g_private){
					$('#main_modal_title').text('This channel already exists. Please select another name.');
				}
				else {
					let el=document.getElementById('channel_password');
					let password=el.value;
					el.value='';
					socket.emit('create_private_channel',{'name':input_val,'password':password})
				}
				break;
		}

	});

	$('#add_channel').on('click',()=>{
		$('#main_modal_title').text('Please enter the channel name');
		$('#main_modal_label').text('Channel Name:')
		let div='<div class="col"><input type="checkbox" id="private_channel_toggle" onclick=""></div>'
		$('#input_row').after(div);
		$('#private_channel_toggle').on('click',()=>{
			if(this.prop('checked')){
				$('#password_row').remove();
			}
			else{
				$('#input_row').after('<div class="row" id="password_row"><div class="col"><input type="text" id="channel_password"></div></div>')
			}
		});
		$('#main_modal').modal('toggle');
	})

	$('#join_private_channel').on('click',()=>{
		$('#main_modal_title').text('Please enter the channel\'s name');
		$('#main_modal_label').text('Channel Name:')
		$('#input_row').after(`<div class="row" id="password_row"><div class="col"><label for="channel_password">Channel Password
			</label><input id="channel_password" type="text"></div></div>`);
		$('#main_modal').modal('toggle');
	});

	socket.on("add_user",data=>{
		if (data['error'] == '') {
			$('#input_row').innerHTML(`<div class="col"><label for="modal_input" id="modal_label">Username</label>
				<input id="modal_input" class="form-control w-50" type="text" data-type=""></div>`)
			$('#main_modal').modal('toggle');
			$('#main_modal_title').txt(data['error']);
		}
		else {
			if( (data['username'] != g_username) || (data['username'] != localStorage.getItem('username')) ){
				add_user(data['username']);
			}
			else{
				localStorage.setItem('username', data['username']);
			}
		}
	});

	socket.on('add_channel',data=>{
		if(data['error'] != ''){
			$('#main_modal').modal('toggle');
			$('#main_modal_title').txt(data['error']);
		}
		else{
			add_channel(data['channel']);
		}
	});
	socket.on('private_channel',data=>{
		if(data['error']!=''){
			$('main_modal').modal('toggle');
			$('#main_modal_title').txt(data['error']);
		}
		else{
			g_private['names'].push(data['channel']);
			g_private['password'].push(data['password']);
			add_channel(data['channel'],true);
		}
	});

	socket.on('user_left',data=>{
		g_users.removeItem(data['username'])
		let username=data['username'].replace(' ','_');
		$('#'+username).remove()
	});

	socket.on('joined',data=>{
		if(data['success']){
			add_messages(data['channel_msgs']);
		}
	});


	socket.on("update_channels",data=>{
		let channels=data['channels'];
		g_channels=channels;
		let max=channels.length;

		for(let i=0;i<max;i++){
			add_channel(channels[i],false);
		}
		//makes the first channel the active one as that's always the one that they join.
		$(`#${g_channels[0]}`).addClass('active');
		channels=data['private_channels'];
		if(channels.length >= 1) {
			for (const full_name in channels) {
				g_private['names'].push(channels[full_name]['name'])
				g_private['passwords'].push(channels[full_name]['password']);
				add_private_channel(channels[full_name]['name'], full_name, channels['password']);
			}
		}
	})

	function pm_user(username_id){
		let username=document.getElementById(username_id).innerText;
		let msg={'username':g_username,'to_user':username}
		if(username in g_users){
			socket.emit('send_pm',msg);
		}
		else{

		}
	}

});
function change_channel(channel){
	let private=$(`#${channel}`).data('private');
	let password='';
	if(private){
		let index=g_private['names'].indexOf(channel);
		password=g_private['passwords'][index];
	}
	$(`#${channel}`).removeClass('active');
	g_current_channel = channel;
	$(`#${channel}`).addClass('active');
	socket.emit('join',{'room':g_current_channel,'password':password});
}

function add_messages(messages){
	let total_messages=messages.length;
	let msgs=''
	for(let i=0;i<total_messages;i++){
		msgs+=contstruct_message(messages[i]);
	}
	$('#msg_block').html(msgs);
}
function construct_message(msg_obj) {
		let user_id=msg_obj['username'].replace(' ','_');
		let msg = `<div class="media d-flex"><div>
		<span><a id="${user_id}" href="#" onclick="message_user(this.id)">${msg_obj['username']}</a></span><span class="pl-2">
			@ ${Date(msg_obj['ts']).toLocalTime()}</span><p>${msg_obj['msg']}</p></div></div>`;
		//msg += '(' + msg_obj['ts'] + ') ' + msg_obj['user'] + ': ' + msg_obj['msg']
		//msg += '</div>'
	return msg;
}

function get_msgs(route, type, data) {
	const req = new XMLHttpRequest();
	req.open(type, route);
	req.send(data)
	req.onload = () => {
		let msgs = '';
		const json_data = JSON.parse(req.responseText)
		if (json_data.success) {
			let total_msgs = json_data.length;
			for (let i = 0;i<total_msgs; i++) {
				msgs += construct_message(msg_obj[i]);
			}
			document.getElementById('messages').innerHTML = msgs;
		}
	}
}

function unbold_channel() {
	document.getElementById(g_current_channel).style.fontWeight = "normal";
}

function bold_channel(){
	document.getElementById(g_current_channel).style.fontWeight = "bold";
}


function add_channel(channel_name,private=false){
	const li=document.createElement('li');
	li.innerText = '#'+channel_name;
	let channel=channel_name.replace(' ','_');
	li.setAttribute('id',channel);
	li.setAttribute('class','list-group-item list-group-item-dark');
	li.setAttribute('onclick','change_channel(this.id)');
	li.setAttribute('data-private',`${private}`);
	$('#channels').append(li);
}

function add_private_channel(short_name,full_name,password){
	const li=document.createElement('li');
	li.innerText = '#'+channel_name;
	let channel=full_name.replace(' ','_');
	li.setAttribute('id',channel);
	li.setAttribute('class','list-group-item list-group-item-dark');
	li.setAttribute('onclick','change_channel(this.id)');
	li.setAttribute('data-private',true);
	$('#channels').append(li);
}

function add_user(username){
	const p=document.createElement('p');
	p.innerText=username;
	p.setAttribute('id',username.replace(' ','_'))
	p.setAttribute('onclick','message_user(this.id)');
	$('#users_online').append(p);
}
function send_msg(){
	let msg = $('#input_box').val;
	if(g_private){
		socket.emit("send_pm");
	}
}
function select_user(){

}
function check_msg(event){
	let key=event.key;
	if (document.getElementById('modal_input').value.length > 0) {
		$("#modal_button").attr('disabled', false);
		if (key === "Enter") {
			send_msg();
		}
	}
	else {
		$("#modal_button").attr('disabled', true);
	}
}