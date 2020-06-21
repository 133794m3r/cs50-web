var g_channels = [];
var g_users = [];
var g_current_channel = "";
var msg_type = "PUBLIC";

function construct_message(msg_obj){
	let msg= '<div class="row">'
	msg+='('+msg_obj['ts']+') '+msg_obj['user']+': '+msg_obj['msg']
	msg+='</div>'
}

function get_msgs(route,type,data){
	const req = new XMLHttpRequest();
	req.open(type,route);
	req.send(data)
	req.onload = () =>{
		let msgs = '';
		const json_data = JSON.parse(req.responseText)
		if(json_data.success){
			let total_msgs = json_data.length;
			for(let i=0;total_msgs;i++){
				msgs+=construct_message(msg_obj[i]);
			}
			document.getElementById('messages').innerHTML = msgs;
		}
	}
}
function unbold_channel(){
	document.getElementById(g_current_channel).style.fontWeight = "normal";
}
function bold_channel(){
	document.getElementById(g_current_channel).style.fontWeight = "bold";
}

function change_channel(channel){
	if(g_channels.includes(g_current_channel)){
		unbold_channel();
	}
	g_current_channel = channel;
	msg_type = "PUBLIC";
	bold_channel();
	document.getElementById('current_channel').innerText = g_current_channel
	localStorage.setItem("channel",g_current_channel);
	get_msgs('/get_messages','POST',channel)
}
