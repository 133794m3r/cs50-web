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
localStorage.clear();
//the globals
var g_channels = [];
var g_pms = {};
var g_pm_msgs = {};
var g_users = [];
var g_current_channel = "";
var g_privates = {'names':[],'passwords':[]};
var g_username = localStorage.getItem('username')
var socket;
var g_private = false;
$('body').ready(()=>{
	document.getElementById('msg_block').scrollTop=3500;
	socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

	if (!g_username){
		console.log('no username')
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
		let input_val=input.val().replace(/\ /g,'_');
		let type=input.data('type');
		input.val('');
		let total_privates = (g_privates["names"] == undefined?0:g_privates["names"].length)
		switch(type){
			case "username":
				//let username=input.val();
				g_username=input_val;
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

				if(input_val in g_channels){
					$('#main_modal_title').text('This channel already exists. Please select another name.');
				}
				else if (total_privates > 0 && input_val in g_private['names']){
					$('#main_modal_title').text('This channel already exists. Please select another name.');
				}
				else {
					console.log('hit');
					socket.emit('create_channel',{'channel':input_val});
				}
				break;

			case "create_private_channel":
				//let name=input.val();
				if(input_val in g_channels){
					$('#main_modal_title').text('This channel already exists. Please select another name.');
				}
				else if (total_privates > 0 && input_val in g_privat['names']){
					$('#main_modal_title').text('This channel already exists. Please select another name.');
				}
				else {
					let el=document.getElementById('channel_password');
					let password=el.value;
					el.value='';
					$('#password_row').remove();
					socket.emit('create_private_channel',{'channel':input_val,'username':g_username,'password':password})
				}
				break;

			case "join_private":
				let password=$('#channel_password').val();
				$('#channel_password').val('');
				if(input_val in g_channels){
					$('#main_modal_title').text("This channel is a regular channel no password is required.")
				}
				else if(password === ''){
					$('#main_modal_title').text("The password cannot be blank.");
				}
				else{
					$('#password_row').remove()
					socket.emit("join",{"channel":input_val,"password":password});
				}
				break;

			case "create_pm":
				let msg=$('#user_message').val();
				$('#pm_row').remove()
				let resp={'username':g_username,'to_user':input_val,'msg':msg};
				socket.emit("create_pm_room",resp);
				break;
		}

	});

	$('#add_channel').on('click',()=>{
		$('#main_modal_title').text('Please enter the channel name');
		$('#modal_label').text('Channel Name:')

		if(document.getElementById('private_channel_toggle') == null){
			let div='<div class="col">Private <input type="checkbox" id="private_channel_toggle" onclick=""></div>'
			$('#input_row').append(div);
		}

		$('#private_channel_toggle').on('click',function(){
			if ($(this).prop('checked')) {
				$('#modal_input').data('type', 'create_private_channel');
				if(document.getElementById('password_row') == null) {
					$('#input_row').after('<div class="row" id="password_row"><div class="col"><label for="channel_password">Password:</label><input type="text" id="channel_password"></div></div>')
				}
			}
			else {
				$('#modal_input').data('type', 'create_channel');
				$('#password_row').remove();
			}
		});
		$('#modal_input').data('type','create_channel');
		console.log('add_channel')
		$('#main_modal').modal('toggle');
	})

	$('#join_private_channel').on('click',()=>{
		$('#main_modal_title').text('Please enter the channel\'s name');
		$('#modal_label').text('Channel Name:')
		if(document.getElementById('password_row') !== null) {
			$('#password_row').remove();
			$('#input_row').after(`<div class="row" id="password_row"><div class="col"><label for="channel_password">Channel Password
			</label><input id="channel_password" type="text"></div></div>`);
		}
		else{
			$('#input_row').after(`<div class="row" id="password_row"><div class="col"><label for="channel_password">Channel Password
			</label><input id="channel_password" type="text"></div></div>`);
		}


		$('#modal_input').data('type','join_private');
		console.log('join private')
		$('#main_modal').modal('toggle');
	});

	socket.on("add_user",data=>{
		if (data['error'] !== '') {
			$('#input_row').html(`<div class="col"><label for="modal_input" id="modal_label">Username</label>
				<input id="modal_input" class="form-control w-50" type="text" data-type="username"></div>`);
			$('#main_modal_title').text(data['error']);
			console.log('cannot add user')
			window.setTimeout(function(){$('#main_modal').modal('toggle');},300);
			//console.log($('#main_modal'));
			//$('#main_modal').removeClass('fade').addClass('show');
			//document.getElementById('main_modal').style='display:block;';

		}
		else {
			console.log(g_username);
			console.log(data['username']);
			if(data['username'] != g_username){
				add_user(data['username']);
			}
			else{
				//add_user(data['username']);
				$('#current_username').text(g_username);
				localStorage.setItem('username',data['username']);
				socket.emit("rejoin",{"username":g_username});
			}
		}
	});
	socket.on('add_channel',data=>{
		if(data['error'] != ''){
			$('#main_modal_title').txt(data['error']);
			console.log('cannot add channel')
			window.setTimeout(function(){$('#main_modal').modal('show');},300);
		}
		else{
			console.log('added channel');
			add_channel(data['channel']);
		}
	});
	socket.on('private_channel',data=>{
		if(data['error']!=''){
			$('#main_modal_title').txt(data['error']);
			console.log('cannot create private channel');
			window.setTimeout(function(){$('#main_modal').modal('show');},300);
		}
		else{
			console.log("added private");
			g_privates['names'].push(data['full_name']);
			g_privates['passwords'].push(data['password']);
			add_private_channel(data['channel'],data['full_name'])
			//add_channel(data['channel'],true);
		}
	});

	socket.on('user_left',data=>{
		g_users.removeItem(data['username'])
		let username=data['username']
		$('#'+username).remove()
	});

	socket.on('joined',data=>{
		if(data['success']){
			console.log('joined');

			if(!g_current_channel){
				g_current_channel=g_channels[0];
			}
			add_messages(data['channel_msgs']);
		}
		else{
			console.log('cannot join')
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

			window.setTimeout(function(){$('#main_modal').modal('show');},300);
		}
	});

	socket.on("add_pm",data=>{
		if(data['error']!=''){
			console.log('cannot pm')
			$('#input_row').html(`<div class="col" id="pm_row"><label for="modal_input" id="modal_label">Username</label>
				<input id="modal_input" class="form-control w-50" type="text" data-type="create_pm"></div>`)
			$('#main_modal_title').text(data['error']);
			window.setTimeout(function(){$('#main_modal').modal('show');},300);
		}
		else{
			let shown_user=data['to'];
			if(shown_user === g_username){
				shown_user=data['from'];
			}
			let channel_id=data['room_name'];
			g_pms[channel_id]={'to':shown_user,'unread':1}
			let html=`<li id="${channel_id}" class="list-group-item list-group-item-dark d-flex justify-content-between
 				align-items-center" onclick="get_pms(this.id)">${shown_user}<span class="badge badge-secondary badge-pill">1
 				</span></li>`
			$('#private_messages').append(html);
			g_pm_msgs[channel_id]=[data['msg']];
		}
	})
	socket.on("pm",data=>{
		if(data['error']!=''){
			console.log('cannot pm')
			$('#input_row').html(`<div class="col" id="pm_row"><label for="modal_input" id="modal_label">Username</label>
				<input id="modal_input" class="form-control w-50" type="text" data-type="pm"></div>`)
			$('#main_modal_title').text(data['error']);
			window.setTimeout(function(){$('#main_modal').modal('show');},300);
		}
		else{
			let shown_user=data['to'];
			if(shown_user === g_username){
				shown_user=data['from'];
			}
			let channel_id=data['room_name'];
			if(g_current_channel !== channel_id) {
				g_pms[channel_id]['msgs'] += 1
			}
			$('#channel_id').text(g_pms[shown_user]);
			g_pm_msgs[channel_id].push(data['msg']);
		}
	});
	socket.on("update_users",data=>{
		console.log('update_users');
		let users=data["users"];
		g_users=g_users.concat(users);
		let total=users.length;
		let q=''
		let p=''
		let username=''
		for(let i=0;i<total;i++){
			username=users[i];
			p=`<p id=${username} onclick="message_user(this.id)">${username}</p>`
			q+=p
		}
		$('#users_online').html(q)
	})
	socket.on("update_channels",data=>{
		let channels=data['channels'];
		g_channels=channels;
		let max=channels.length;
		console.log("adding channels");
		for(let i=0;i<max;i++){
			add_channel(channels[i],false);
		}
		//makes the first channel the active one as that's always the one that they join.
		$(`#${g_channels[0]}`).addClass('active');
		channels=data['private_channels'];
		if(channels.length >= 1) {
			for (const full_name in channels) {
				g_privates['names'].push(channels[full_name]['name'])
				g_privates['passwords'].push(channels[full_name]['password']);
				add_private_channel(channels[full_name]['name'], channels[full_name]['full_name'], channels['password']);
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
		let index=g_privates['names'].indexOf(channel);
		password=g_privates['passwords'][index];
	}
	console.log(channel);
	console.log(g_current_channel);
	$(`#${g_current_channel}`).removeClass('active');
	$(`#${channel}`).addClass('active');

	g_current_channel = channel;

	socket.emit('join',{'channel':g_current_channel,'password':password});
}

function add_messages(messages){
	let total_messages=messages.length;
	let msgs=''
	for(let i=0;i<total_messages;i++){
		msgs+=construct_message(messages[i]);
	}
	$('#msg_block').html(msgs);
	document.getElementById('msg_block').scrollTop=35000000;
}
function construct_message(msg_obj) {
		let user_id=msg_obj['username'];
		let msg = `<div class="media d-flex"><div>
		<span><a id="${user_id}" href="#" onclick="message_user(this.id)">${msg_obj['username']}</a></span><span class="pl-2">
			@ ${new Date(parseInt(msg_obj['time'])).toLocalTime()}</span><p>${msg_obj['text']}</p></div></div>`;
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
	li.setAttribute('id',channel_name);
	li.setAttribute('class','list-group-item list-group-item-dark');
	li.setAttribute('onclick','change_channel(this.id)');
	li.setAttribute('data-private',`${private}`);
	$('#channels').append(li);
}

function add_private_channel(short_name,full_name){
	const li=document.createElement('li');
	li.innerText = '#'+short_name;
	li.setAttribute('id',full_name);
	li.setAttribute('class','list-group-item list-group-item-dark');
	li.setAttribute('onclick','change_channel(this.id)');
	li.setAttribute('data-private',true);
	$('#channels').append(li);
}

function add_user(username){
	const p=document.createElement('p');
	p.innerText=username;
	p.setAttribute('id',username)
	p.setAttribute('onclick','message_user(this.id)');
	$('#users_online').append(p);
}
function send_msg(){
	let msg = $('#input_box').val();
	$('#input_box').val('');
	console.log(msg);
	if(g_private){
		let to_user=g_pms[g_current_channel]['to']
		socket.emit("send_pm",{'username':g_username,'to':to_user,'msg':msg});
	}
	else{
		socket.emit("submit_to_room",{'channel':g_current_channel,'username':g_username,'msg':msg});
	}
}
function select_user(){

}
function update_msg(event){
	let key=event.key;
	//console.log(key);
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

function message_user(username){
	if(username !== g_username){
		$('#input_row').html(`<div class="col"><label for="modal_input" id="modal_label">Username</label>
			<input id="modal_input" class="form-control w-50" type="text" data-type="create_pm" value="${username}"></div>`);
		$('#message_row').after('');
		$('#input_row').after(`<div class="row" id="message_row"><div class="col"><label for="user_message">Your Message
		</label><input id="user_message" type="text"></div></div>`);
		$('#main_modal_title').text(`Sending message to ${username}`);
		$("#user_message").on('keyup', function (event){
			console.log(event.key);
			if (document.getElementById('user_message').value.length > 0) {
				$("#modal_button").attr('disabled', false);

				if (event.key === 'Enter') {
					$('#modal_button').click();
				}
			}
			else {
				$("#modal_button").attr('disabled', true);
			}
		});

		$('#main_modal').modal('toggle');
	}
}
function get_pms(room_id){
	g_private = true;
	let msgs=g_pm_msgs[room_id];
	$(`#${g_current_channel}`).removeClass('active');
	g_current_channel=room_id;
	g_pms[g_current_channel]['msgs']=0;
	$(`#${room_id}`).addClass('active');
	add_messages(msgs);
}
