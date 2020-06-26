import os

from flask import Flask,jsonify,request,render_template
import time,json
from flask_socketio import SocketIO, emit,join_room,leave_room
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socket = SocketIO(app)
#the total "global" channels.
channels_list = ["main"]
#the private channels that people can create.
#each one has a name and also the password to join it.
"""
There are 2 keys. One that maps the channel's true name(name given by the user
16 bits from socke.io sid). Then the other major key is the passwords. An 
example is below.
{
	"names":{
			"test_channela1345df":"test_channel"
	}
	"passwords":{
			"test_channel1345df":"password"
	}
}
Basically the "passwords" dictionary holds the channel's truename and the
password to join it. Whereas names maps it in the exact opposite fashion. When
a user gives someone an invite what they are actually giving them is the channel
name. Plus the other data is embedded within the link when they join it.
"""
private_channels = {"names":{},
                    "passwords":{}
                    }
"""
User Private messages. It's a list of all current PMs that users are currently 
doing.  It's name is simply the concentation of the sid(s) of the 2 users and 
it. Then it contains the 2 session ids that we should broadcast to so that don't
let someone join the room w/o access.  
"""
user_pms = {}

"""
Users dictionary
It basically looks like this. Where request.sid is the socketio session id.
users[<username>] = request.sid
"""
users = {}

"""
A dictionary that holds the rooms that the user has passwords to/has connected 
to previously. It holds the rooms that they can connect to automatically upon 
reconnecting. It holds the rooms that they have passwords to.

users_rooms = { <username>:[<list>,<of>,<roms>]}
"""
users_rooms = {}

"""
Here we have all of the channel messages each channel's messages as their own
named item. This is to avoid having everything sent to the user each time a 
request is sent to them. Plus it contains the number of messages in each of the
channels.
"""
channels_msgs = {
	"main": {
		"num_msgs":0,
		"msgs":[]
		}
}
#How many messages we're going to allow each channel to have.
msg_limit = 100

def private_channels_info(rooms_list):
	#private_channels.items()
	private_info=[]
	tmp={}
	for room in rooms_list:
		tmp[room]={}
		tmp[room]['name']=private_channels['names'][room]
		tmp[room]['password']=private_channels["passwords"][room]
		private_info.append(tmp)

	return private_info

def update_room_msg(data,room):
	msg = {'text': data['msg'], 'username': data['username'], 'time': data['time']}
	if channels_msgs[room]['num_msgs'] >= 50:
		channels_msgs[room]['msgs'].pop(0)
	else:
		channels_msgs[room]['num_msgs'] += 1
	channel_msgs[room]["msgs"].append(msg)

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/get_channels",methods=["GET"])
def get_channels():
	return jsonify({'success':True,"channels":channels_list})

@app.route("/get_messages",methods=["POST"])
def get_messages():
	pass

@app.route("/get_users",methods=["GET"])
def get_users():
	pass

@socket.on("connect")
def connect():
	print('connecting')
	emit("connect",{'msg':'a'})

@socket.on("rejoin")
def reconnect(data):
	channel=channels_list[0]
	join_room(channel)
	username=data['username']
	private_rooms=users_rooms.get('username')
	if private_rooms:
		private_rooms=private_channels_info(private_rooms)
	else:
		private_rooms={}
	emit("update_channels",{"channels":channels_list,"private_channels":private_rooms},room=request.sid)
	emit("joined",{"success":True,"channel_msgs":channels_msgs[channel]['msgs']},room=request.sid)

@socket.on("join")
def join(data):
	if data == "":
		send("joined",{success:False,"error":"Response was not received","channel_msgs":""},room=request.sid)
	room = data["channel"]
	if room not in channels_list:
		if room not in private_channels:
			send("joined",{success:False,"error":"Invalid room selected.","channel_msgs":""},room=request.sid)
		else:
			if data["password"] != private_channels[room]["password"]:
				send("joined", {success: False, "error": "Invalid password provided.", "channel_msgs": ""}, room=request.sid)

	join_room(room)

	emit("joined",{"success":True,"channel_msgs":channel_msgs[channel]['msgs']},room=request.sid)

@socket.on("leave")
def leave(data):
	room = data['channel']
	leave_room(room)

	update_room_msg(data,room)
	emit('left',{'channel',channels_msgs[room]['msgs']},room=room)

@socket.on("send_to_main")
def submit_to_all(data):
	update_room_msg(data,"main")
	emit("send_to_main",{"channel_msgs":channels_msgs['main']['msgs']},broadcast=True)

@socket.on("submit_to_room")
def submit_to_room(data):
	room=data['channel']
	update_room_msg(data,room)
	emit("announce_room",{"channel_msgs":channels_msgs[room]['msgs']})

@socket.on("rejoin_general")
def rejoin_general():
	emit("announce_to_main",{"channel_msgs":channels_msgs['main']['msgs']},broadcast=True)
	
@socket.on("create_channel")
def create_channel(data):
	error_str=""
	channel=data["channel"]
	if channel == "" or channel is None:
		error_str="No data received"
	elif channel in channels_list or channel in private_channels:
		error_str="Channel cannot already exist"
	else:
		channels_list.append(channel)

		channels_msgs[channel]={'num_msgs':0,msgs:[]}
	if error_str != "":
		send("add_channel",{"channel":channel,"error":error_str},room=request.sid)
	else:
		emit("add_channel",{"channel":channel,"error":""},broadcast=True)

@socket.on("new_user")
def new_user(data):
	username=data.get('username')
	error=""
	if username is None:
		error = "No username provided."
	elif data['username'] in users:
		error = "Username already exists."
	else:
		users[username] = request.sid
		users_rooms['username']=[]

	if error != "":
		emit('add_user',{'username':username,'error':''},broadcast=True)
	else:
		emit('add_user',{'username':username,'error':error},room=request.sid)

@socket.on("create_private_channel")
def create_private_channel(data):
	channel_name=data.get('channel_name')
	full_name=channel_name+request.sid[0:8]
	password=data.get('password')
	msg={"msg":"","error":""}
	if channel_name is None or channel_name == "":
		msg["error"]="No channel name given."
	elif channel_name in channels_list:
		msg["error"] = "Channel name must be unique and not mirror any of the generals."
	elif full_name in private_channels["names"]:
		msg["error"] = "Error your channel name must be unique."
	else:
		private_channels["names"][full_name]=channel_name
		private_channels["passwords"][full_name]=password
		socket.server.enter_roomt(request.sid,full_name)
		msg['password']=password
		msg['msg']=f"Channel {channels_name} created with password {password}"
		users_rooms['username'].append(full_name)

	emit("private_channel",msg,room=request.sid)

@socket.on('create_pm_room')
def create_pm_room(data):
	sender=data.get('username')
	receiver=data.get('to_username')
	if receiver not in users:
		pass
	pass

@socket.on("send_pm")
def private_msg(data):
	sender=data.get('username')
	receiver=data.get('to_user')
	if receiver not in users:
		emit("pm",{'error':'User not found','msg':''},room=request.sid)
	else:
		room=users[receiver]+users[sender]
		channels_msgs[room]={
			msgs:[],
			num_msgs:[]
		}
		socket.server.enter_room(users[receiver],room)
		socket.server.enter_room(request.sid,room)
		#message = {'text': data['msg'], 'sender': sender, 'time': data['time'],'error':''}
		message={'room_name':room,'from':sender,'to':receiver}
		emit("pm",message,room=room)

@socket.on("update_user_channels")
def update_user_channels(data):
	pass
		
@socket.on("client_disconnect")
def client_disconnect(data):
	username=data.get('username')
	if username is not None:
		emit("user_left",{'username':username})
	pass