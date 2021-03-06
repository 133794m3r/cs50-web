
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
var g_pm_msgs = {};
var g_users = [];
//sets the current channel to the one stored within the local storage.
var g_current_channel = localStorage.getItem("current_channel");
var g_privates = {'names':[],'passwords':[],'full_name':[]};
//same with the username.
var g_username = localStorage.getItem('username')
var socket;
var g_private = false;

//once it's all setup I have this function wait till everything else is loaded before I start doing things.
$('body').ready(()=>{
	document.getElementById('msg_block').scrollTop=100000000000;
	//create the actual socket.
	socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

	//if they don't already have a username.
	if (!g_username){
		console.log('no username');
		//prompt them for one.
		$("#main_modal").modal('toggle');
		$('#modal_input').data('type','username');
	}
	else{
		//otherwise add them to the list of users
		add_user(g_username)
		//and make them rejoin all of their channels.
		socket.emit('rejoin',{'username':g_username,'channel':g_current_channel});
	}

	$('#modal_button').on('click',()=>{
		let input=$("#modal_input");
		let input_val=input.val().replace(/\ /g,'_');
		let type=input.data('type');
		input.val('');
		let total_privates = (g_privates["names"] == undefined?0:g_privates["names"].length)
		//switch through types till I figure out which one it is to properly emit the data on the socket.
		switch(type){
			//new username/bad username.
			case "username":
				//let username=input.val();
				g_username=input_val;
				if(input_val in g_users){
					//tell them that the username already exists and.
					$('#main_modal_title').text('This user already exists. Please select another.');
				}
				else {
					//try to create the user on the server.
					socket.emit('new_user', {'username': input_val});
				}
				break;

			//the case where they're joining a channel through the button.
			case "join_channel":
				if(g_channels.indexOf(input_val) !== -1){
					//can't recreate a channel that already exists.
					$('#main_modal_title').text('This channel doesn\'t exist. Please check your spelling');
				}
				else{
					//do the join event with this channel.
					socket.emit("join",{'channel':input_val});
				}
				break;

			case "create_channel":
				//let name=input.val();
				//when they're creating a channel.
				if(g_channels.indexOf(input_val)!== -1){
					//already have it existing in the general channels.
					$('#main_modal_title').text('This channel already exists. Please select another name.');
				}
				else if ((total_privates > 0) && (g_private['names'].indexOf(input_val) !== -1)){
					//it already existed in the private channels they're a member of. This prevents them from creating a channel
					//with the same name as one they're already in/aware of.
					$('#main_modal_title').text('This channel already exists. Please select another name.');
				}
				else {
					//create teh channel.
					socket.emit('create_channel',{'channel':input_val});
				}
				break;

			case "create_private_channel":
				//let name=input.val();
				//see if the channel exists in the global channels.
				if(g_channels.indexOf(input_val) !== -1){
					$('#main_modal_title').text('This channel already exists. Please select another name.');
				}
				else if ((total_privates > 0)&& (g_privates['names'].indexOf(input_val) !== -1)){
					//same here don't let them create a channel with the same name.
					$('#main_modal_title').text('This channel already exists. Please select another name.');
				}
				else {
					//otherwise it's time to try and create it.
					let el=document.getElementById('channel_password');
					//get the password value.
					let password=el.value;
					//reset it to blank.
					el.value='';
					//remove that row.
					$('#password_row').remove();
					//emit the event to create the channel with the name, their username and the password.
					socket.emit('create_private_channel',{'channel':input_val,'username':g_username,'password':password})
				}
				break;

			case "join_private":
				//this is when they try to join a private channel.
				let password=$('#channel_password').val();
				$('#channel_password').val('');
				//the channel must not be a public one.
				if(g_channels.indexOf(input_val) !== -1){
					$('#main_modal_title').text("This channel is a regular channel no password is required.")
				}
				else if(password === ''){
					//the password can't be blank.
					$('#main_modal_title').text("The password cannot be blank.");
				}
				else{
					//remove the password row.
					$('#password_row').remove()
					//emit the join event with the password and their username so that the server can add it to their list of joined
					//channels.
					socket.emit("join",{"username":g_username,"channel":input_val,"password":password});
				}
				break;

			case "create_pm":
				//when they create a private message to a new user.
				let msg=$('#user_message').val();
				//remove the room row.
				$('#pm_row').remove()
				//remove the message row.
				$('#message_row').remove()
				//emit the event to the server with who it was from, and who it was to. Also send the message to the server.
				let resp={'username':g_username,'to_user':input_val,'msg':msg};
				let to_user=''
				let found=false
				for(let key in g_pms){
					to_user = g_pms[key]['to'];
					if(to_user === input_val){
						found=true;
						socket.emit("pm",resp);
						break;
					}
				}
				//emit the event to the server.
				if(!found){
					socket.emit("create_pm_room", resp);
				}
				break;
		}

	});

	//when the add channel button is clicked do this.
	$('#add_channel').on('click',()=>{
		//create the modal for the add channel event.
		$('#main_modal_title').text('Please enter the channel name');
		$('#modal_label').text('Channel Name:')
		$('#input_row')
		$('.row2').remove()
		if(document.getElementById('private_channel_toggle') == null){
			let div='<div class="col">Private <input type="checkbox" id="private_channel_toggle" onclick=""></div>'
			$('#input_row').append(div);
		}
		//if they click the private room checkbox then it'll toggle the password rwo.
		$('#private_channel_toggle').on('click',function(){
			if ($(this).prop('checked')) {
				$('#modal_input').data('type', 'create_private_channel');
				if(document.getElementById('password_row') == null) {
					$('#input_row').after('<div class="row row2" id="password_row"><div class="col"><label for="channel_password">Password:</label><input type="text" id="channel_password"></div></div>')
				}
			}
			else {
				$('#modal_input').data('type', 'create_channel');
				$('#password_row').remove();
			}
		});
		//set the type to create channel.
		$('#modal_input').data('type','create_channel');
		console.log('add_channel')
		//toggle the modal after it's all drawn.
		$("#main_modal").modal('toggle');
	});

	//when they try to join it setup this modal.
	$('#join_private_channel').on('click',()=>{
		$('.row2').remove();
		$('#main_modal_title').text('Please enter the channel\'s name');
		$('#modal_label').text('Channel Name:');
		//make sure the toggle is checked.
		$('#private_channel_toggle').checked(true);
		if(document.getElementById('password_row') !== null) {
			$('#password_row').remove();
			$('#input_row').after(`<div class="row row2" id="password_row"><div class="col"><label for="channel_password">Channel Password
			</label><input id="channel_password" type="text"></div></div>`);
		}
		else{
			$('#input_row').after(`<div class="row row2" id="password_row"><div class="col"><label for="channel_password">Channel Password
			</label><input id="channel_password" type="text"></div></div>`);
		}

		$('#modal_input').data('type','join_private');
		console.log('join private')
		$("#main_modal").modal('toggle');
	});
	//the first of our socket events. This one is when the user already exists event.
	socket.on("user_exists",data=>{
		//clear their local storage as it's invalid.
		localStorage.clear()
		//create the information modal to help them realize that they have this error.
		$('#input_row').html(`<div class="col"><label for="modal_input" id="modal_label">Username</label>
			<input id="modal_input" class="form-control w-50" type="text" data-type="username" onkeypress="modal_update(event)"></div>`);
		$('#main_modal_title').text(data['error']);
		console.log('user already exists')
		window.setTimeout(function(){$("#main_modal").modal('toggle');},300);

	});

	//the add user event.
	socket.on("add_user",data=>{
		//if data['error'] is anything but empty string then it's an error.
		if (data['error'] !== '') {
			$('#input_row').html(`<div class="col"><label for="modal_input" id="modal_label">Username</label>
				<input id="modal_input" class="form-control w-50" type="text" data-type="username" onkeypress="modal_update(event)"></div>`);
			$('#main_modal_title').text(data['error']);
			console.log('cannot add user')
			window.setTimeout(function(){$("#main_modal").modal('toggle');},300);

		}
		else {
			//otherwise we add the user to the list/set if it's no the same as our own.
			console.log(g_username);
			console.log(data['username']);
			if(data['username'] != g_username){
				add_user(data['username']);
			}
			else{
				//add_user(data['username']);
				$('#current_username').text(g_username);
				//set the property as their username.
				localStorage.setItem('username',data['username']);
				//rejoin event is fired to rejoin all channels.
				socket.emit("rejoin",{"username":g_username});
			}
		}
	});

	//a channel was added.
	socket.on('add_channel',data=>{
		//error means they did something wrong/something went wrong.
		if(data['error'] != ''){
			$('#main_modal_title').text(data['error']);
			console.log('cannot add channel')
			window.setTimeout(function(){$("#main_modal").modal('show');},300);
		}
		else{
			//add teh channel to the list.
			console.log('added channel');
			g_channels.push(data['channel']);
			add_channel(data['channel']);
		}
	});

	//the private channel socket event for when they create a private channel.
	socket.on('private_channel',data=>{
		//error means something was broke.
		if(data['error']!=''){
			$('#main_modal_title').text(data['error']);
			console.log('cannot create private channel');
			window.setTimeout(function(){$("#main_modal").modal('show');},300);
		}
		else{
			//add the private information to the global object.
			console.log("added private");
			g_privates['full_name'].push(data['full_name']);
			g_privates['names'].push(data['channel']);
			g_privates['passwords'].push(data['password']);
			add_private_channel(data['channel'],data['full_name'])
			//add_channel(data['channel'],true);
		}
	});
	//a user has left. For some reason this doesn't always get sent by the server.
	socket.on('user_left',data=>{
		console.log("user left");
		g_users.removeItem(data['username'])
		let username=data['username']
		$('#'+username).remove()
	});

	//they joined a channel event.
	socket.on('joined',data=>{
		//it worked. I should make them all have a success property but I didn't in time. Maybe for 1.1 version.
		if(data['success']){
			console.log('joined');
			//if the current channel isn't already set.
			if(!g_current_channel){
				//set it as the first channel in the list.
				g_current_channel=g_channels[0];
			}
			//add all of the messages from the channel.
			add_messages(data['channel_msgs']);

		}
		else{
			//otherwise we have to setup the error modal.
			let channel=data['channel'];
			let password=data['password'];
			$('#main_modal_title').text(data['error']);
			$('#modal_label').text('Channel Name:');
			$('#modal_input').val(channel);
			$('.row2').remove();
			//password is not empty means it's a private room.
			if(password !== ''){
				$('#input_row').after(`<div class="row row2" id="password_row"><div class="col"><label for="channel_password">
					Channel Password</label><input id="channel_password" type="text"></div></div>`);
				$('#modal_input').data('type','join_private');
			}
			else{
				$('#modal_input').data('type','join_channel');
			}
			//we have to delay it by some amount of time to get it to reopen properly.
			window.setTimeout(function(){$("#main_modal").modal('show');},300);
		}
	});

	//someone pmed someone.
	socket.on("add_pm",data=>{
		//error means it didn't work.
		if(data['error']!=''){
			console.log('cannot pm');
			$('#input_row').html(`<div class="col" id="pm_row"><label for="modal_input" id="modal_label">Username</label>
				<input id="modal_input" class="form-control w-50" type="text" data-type="create_pm" onkeypress="modal_update(event)"></div>`)
			$('#main_modal_title').text(data['error']);
			window.setTimeout(function(){$("#main_modal").modal('show');},300);
		}
		else{
			//otherwise we have to add the first PM.
			let shown_user=data['to'];
			//set msg count to 1.
			let msgs=1;
			//see if the event was sent back to the sender or other person.
			if(shown_user === g_username){
				//if it is then we set the msg count to zero since they would've already seen it.
				shown_user=data['from'];
				msgs=0;
			}
			//the channel_id is the full name of their room during PMing.
			let channel_id=data['room_name'];
			g_pms[channel_id]={'to':shown_user,'msgs':1}
			//a template string that has the channel id(which is used to get the PMs), and also the counter.
			let html=`<li id="${channel_id}" class="list-group-item list-group-item-dark d-flex justify-content-between
 				align-items-center" onclick="get_pms(this.id)">${shown_user}<span class="badge badge-secondary badge-pill">${msgs}
 				</span></li>`
			//append the new PM room to the list of them.
			$('#private_messages').append(html);
			g_pm_msgs[channel_id]=[data['msg']];
		}
	});

	//a new PM is sent.
	socket.on("pm",data=>{
		//error was occured.
		if(data['error']!=''){
			//couldn't send the PM.
			console.log('cannot pm')
			$('#input_row').html(`<div class="col" id="pm_row"><label for="modal_input" id="modal_label">Username</label>
				<input id="modal_input" class="form-control w-50" type="text" data-type="pm" onkeypress="modal_update(event)"></div>`)
			$('#main_modal_title').text(data['error']);
			window.setTimeout(function(){$("#main_modal").modal('show');},300);
		}
		else{
			//otherwise again figure out who this was to/form.
			let shown_user=data['to'];
			//it was to them so we set the displayed user as the person who sent it.
			if(shown_user === g_username){
				shown_user=data['from'];
			}
			//get the channel id.
			let channel_id=data['room_name'];
			//see if the current channel is that channel if it is no reason to increment unread count.
			if(g_current_channel !== channel_id) {
				//increment unread count by 1.
				g_pms[channel_id]['msgs'] += 1
				//set inner text to the current count of unread messages.
				$(`#${channel_id}`).find("span").text(g_pms[channel_id]['msgs']);
			}
			//make sure it scrolls to the top.
			document.getElementById('msg_block').scrollTop=100000000000;
			$('#channel_id').text(g_pms[shown_user]);
			g_pm_msgs[channel_id].push(data['msg']);
			//if they're in that channel add the message to their display.
			if(g_current_channel === channel_id){
				add_message(data['msg']);
			}
		}
	});

	//update the list of users.
	socket.on("update_users",data=>{
		let users=data["users"];
		g_users=g_users.concat(users);
		let total=users.length;
		let q=''
		let p=''
		let username=''
		//create teh list of users.
		for(let i=0;i<total;i++){
			username=users[i];
			p=`<p id=${username} onclick="message_user(this.id)">${username}</p>`
			q+=p
		}
		//append them to the list.
		$('#users_online').html(q)
	});

	//same but for channels.
	socket.on("update_channels",data=>{
		let channels=data['channels'];
		g_channels=channels;
		let max=channels.length;
		console.log("adding channels");
		for(let i=0;i<max;i++){
			add_channel(channels[i],false);
		}
		//makes the current channel as active.
		$(`#${g_current_channel}`).addClass('active');
		channels=data['private_channels'];
		console.log(data);
		let full_names=data['private_channels']['full_names'];
		console.log(full_names)
		if(full_names == undefined){
			return;
		}

		let channels_length=full_names.length;
		let full_name = ''
		//if there's more than 1 private channel then we need to add those too.
		if(channels_length >= 1) {
			for (let i=0;i<channels_length;i++) {
				full_name=full_names[i];
				g_privates['full_name'].push(full_name);
				g_privates['names'].push(channels[full_name]['name'])
				g_privates['passwords'].push(channels[full_name]['password']);
				add_private_channel(channels[full_name]['name'],full_name, channels['password']);
			}
		}
	});

	//add the message that someone sent to the current room.
	socket.on("announce_room",data=>{
		add_message(data['msg']);
	});

});

function change_channel(channel){
	let private=$(`#${channel}`).data('private');
	let password='';

	if(private){
		let index=g_privates['names'].indexOf(channel);
		password=g_privates['passwords'][index];
	}

	$(`#${g_current_channel}`).removeClass('active');
	$(`#${channel}`).addClass('active');
	g_private = false;
	g_current_channel = channel;
	localStorage.setItem("current_channel",g_current_channel);
	socket.emit('join',{'username':g_username,'channel':g_current_channel,'password':password});
}

function add_message(message){
	$('#msg_block').append(construct_message(message));
	document.getElementById('msg_block').scrollTop=100000000000;
}

function add_messages(messages){
	let total_messages=messages.length;
	let msgs=''
	for(let i=0;i<total_messages;i++){
		msgs+=construct_message(messages[i]);
	}

	$('#msg_block').html(msgs);
	document.getElementById('msg_block').scrollTop=100000000000;
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

function join_channel(channel_name,password=''){
	$(`#${g_current_channel}`).removeClass('active');
	$(`#${channel_name}`).addClass('active');
	g_current_channel=channel_name
	localStorage.setItem("current_channel",g_current_channel);
	if(password !== ''){
		socket.emit('join',{'channel':channel_name,'username':g_username,'password':password});
	}
	else{
		socket.emit('join',{'channel':channel_name,'username':g_username});
	}

}

function msg_join_channel(msg){
	const regex = RegExp('\!join\ #([A-Za-z0-9\-\_][^ ]+)','g');
	let matches=[];
	let replace_str='';
	let index=0;
	let full_name='';
	let password='';
	while((matches = regex.exec(msg))!== null){
		console.log(matches.join(','));
		if(g_channels.indexOf(matches[1]) !== -1){
			index=g_channels.indexOf(matches[1]);
			replace_str=`join <a href="#" title="Join ${g_channels[index]}" 
				onclick="join_channel('${g_channels[index]}'); return false">#${g_channels[index]}</a>`
			console.log(replace_str);
			console.log(msg.replace(matches[0],replace_str));
			msg=msg.replace(matches[0],replace_str);
		}
		else if(g_privates['names'].indexOf(matches[1]) !== -1){
			index=g_privates['names'].indexOf(matches[1]);
			full_name=g_privates['full_name'][index];
			password=g_privates['passwords'][index];
			replace_str=`join <a href="#" title="Join ${full_name}" onclick="join_channel('${full_name}','${password}'); return false">
			#${matches[1]}</a>`
			console.log(replace_str);
			msg=msg.replace(matches[0],replace_str);
		}
	}
	return msg;
}

function send_msg(){
	let msg = $('#input_box').val();
	$('#input_box').val('');
	console.log(msg);
	msg=msg_join_channel(msg);
	if(g_private){
		let to_user=g_pms[g_current_channel]['to']
		socket.emit("send_pm",{'room':g_current_channel,'username':g_username,'to_user':to_user,'msg':msg});
	}
	else{
		socket.emit("submit_to_room",{'channel':g_current_channel,'username':g_username,'msg':msg});
	}
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
			<input id="modal_input" class="form-control w-50" type="text" data-type="create_pm" value="${username}" onkeypress="modal_update(key)"></div>`);
		$('.row2').remove()

		$('#input_row').after(`<div class="row row2" id="message_row"><div class="col"><label for="user_message">Your Message
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

		$("#main_modal").modal('toggle');
	}
}

function get_pms(room_id){
	g_private = true;
	let msgs=g_pm_msgs[room_id];
	$('#msg_block').html('')
	$(`#${g_current_channel}`).removeClass('active');
	g_current_channel=room_id;
	g_pms[g_current_channel]['msgs']=0;
	$(`#${g_current_channel}`).find("span").text(0);
	$(`#${room_id}`).addClass('active');
	add_messages(msgs);
}

function modal_update(key){
	if (document.getElementById('modal_input').value.length > 0) {
		$("#modal_button").attr('disabled', false);
		if (key.keyCode === 13) {
			$('#modal_button').click();
		}
	}
	else {
		$("#modal_button").attr('disabled', true);
	}
}
