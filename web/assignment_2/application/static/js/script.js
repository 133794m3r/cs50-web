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
var g_pms = {};
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
		let type=input.data('type');
		switch(type){
			case "username":
				//let username=input.val();
				if(input_val in g_users){
					$('#main_modal_title').text('This user already exists. Please select another.');
				}
				else {
					socket.emit('new_user', {'username': input_val});
				}
				break;
			case "join_channel":
				if(! (input_val in g_channels)){
					$('#main_modal_title').text('This channel doesn\'t exist. Please check your spelling');
				}
				else{
					socket.emit("join",{'channel':input_val});
				}
			case "create_channel":
				//let name=input.val();
				if(input_val in g_channels || input_val in g_private){
					$('#main_modal_title').text('This channel already exists. Please select another name.');
				}
				else {
					socket.emit('new_channel',{'channel':input_val});
				}
				break;

			case "create_private_channel":
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

			case "join_private":
				let password=$('#channel_password').val();
				if(input_val in g_channels){
					$('#main_modal_title').text("This channel is a regular channel no password is required.")
				}
				else if(password === ''){
					$('#main_modal_title').text("The password cannot be blank.");
				}
				else{
					socket.emit("join",{"room":input_val,"password":password});
				}
				break;

			case "create_pm":
				let msg=$('#user_message').val();
				let resp={'username':g_username,'to_user':input_val,'msg':msg};
				socket.emit("create_pm_room",resp);
				break;
		}

	});

	$('#add_channel').on('click',()=>{
		$('#main_modal_title').text('Please enter the channel name');
		$('#modal_label').text('Channel Name:')
		let div='<div class="col"><input type="checkbox" id="private_channel_toggle" onclick=""></div>'
		$('#input_row').after(div);
		$('#private_channel_toggle').on('click',()=>{
			if(this.prop('checked')){
				$('#modal_input').data('type','create_channel');
				$('#password_row').remove();
			}
			else{
				$('#modal_input').data('type','create_private_channel');
				$('#input_row').after('<div class="row" id="password_row"><div class="col"><input type="text" id="channel_password"></div></div>')
			}
		});
		$('#modal_input').data('type','channel');
		$('#main_modal').modal('toggle');
	})

	$('#join_private_channel').on('click',()=>{
		$('#main_modal_title').text('Please enter the channel\'s name');
		$('#modal_label').text('Channel Name:')
		$('#input_row').after(`<div class="row" id="password_row"><div class="col"><label for="channel_password">Channel Password
			</label><input id="channel_password" type="text"></div></div>`);
		$('#modal_input').data('type','join_private');
		$('#main_modal').modal('toggle');
	});

	socket.on("add_user",data=>{
		if (data['error'] == '') {
			$('#input_row').innerHTML(`<div class="col"><label for="modal_input" id="modal_label">Username</label>
				<input id="modal_input" class="form-control w-50" type="text" data-type="username"></div>`)
			$('#main_modal_title').txt(data['error']);
			$('#main_modal').modal('toggle');
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
			$('#main_modal_title').txt(data['error']);
			$('#main_modal').modal('toggle');
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
			g_current_channel=g_channels[0];
			add_messages(data['channel_msgs']);
		}
		else{
			let channel=data['channel'];
			let password=data['password'];
			$('#main_modal_title').text(data['error']);
			$('#modal_label').text('Channel Name:');
			$('#modal_input').val(channel);
			if(password === ''){
				$('#input_row').after(`<div class="row" id="password_row"><div class="col"><label for="channel_password">
					Channel Password</label><input id="channel_password" type="text"></div></div>`);
				$('#modal_input').data('type','join_private');
			}
			else{
				$('#modal_input').data('type','join_channel');
			}

			$('#main_modal').modal('toggle');
		}
	});

	socket.on("add_pm",data=>{
		if(data['error']!=''){
			$('#input_row').innerHTML(`<div class="col"><label for="modal_input" id="modal_label">Username</label>
				<input id="modal_input" class="form-control w-50" type="text" data-type="create_pm"></div>`)
			$('#input_row').after(`<div class="row" id="message_row"><div class="col"><label for="user_message">Your Message
			</label><input id="user_message" type="text"></div></div>`);
			$('#main_modal_title').txt(data['error']);
			$('#main_modal').modal('toggle');
		}
		else{
			let shown_user=data['to_user'];
			if(shown_user === g_username){
				g_pms[data['from_user']]=1;
				shown_user=data['from_user'];
			}
			else{
				g_pms[data['from_user']]=1;
			}
			let channel_id=data['room_name'];
			let html=`<li class="list-group-item list-group-item-dark d-flex justify-content-between align-items-center">
				${shown_user}<span class="badge badge-secondary badge-pill">1</span></li>`
			$('#private_messages').append(html)
		}
	})
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
	socket.on("announce_room",data=>{
		add_messages(data['channel_msgs']);
	})
	function pm_user(username_id){
		let username=document.getElementById(username_id).innerText;
		let msg=$('#input_box').val();
		let resp={'username':g_username,'to_user':username,'msg':msg};

		if(username in g_users){
			if(username in g_pms) {
				socket.emit('send_pm', resp);
			}
			else{
				socket.emit("create_pm_room",resp);
			}
		}
		else{
			socket.emit("create_pm_room",resp);
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
		msgs+=construct_message(messages[i]);
	}
	$('#msg_block').html(msgs);
}
function construct_message(msg_obj) {
	console.log(msg_obj);
		let user_id=msg_obj['username'].replace(' ','_');
		let msg = `<div class="media d-flex"><div>
		<span><a id="${user_id}" href="#" onclick="message_user(this.id)">${msg_obj['username']}</a></span><span class="pl-2">
			@ ${new Date(parseInt(msg_obj['time'])).toLocalTime()}</span><p>${msg_obj['text']}</p></div></div>`;
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
	let msg = $('#input_box').val();
	$('#input_box').val('');
	console.log(msg);
	if(g_private){
		socket.emit("send_pm",msg);
	}
	else{
		socket.emit("submit_to_room",{'channel':g_current_channel,'username':g_username,'msg':msg});
	}
}
function select_user(){

}
function update_msg(event){
	let key=event.key;
	if (document.getElementById('input_box').value.length > 0) {
		$("#input_button").attr('disabled', false);
		if (key == "Enter") {
			send_msg();
		}
	}
	else {
		$("#input_button").attr('disabled', true);
	}
}