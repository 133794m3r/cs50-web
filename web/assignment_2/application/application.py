import os

from flask import Flask,jsonify,request,render_template,session
from flask_session import Session
import time,json
from flask_socketio import SocketIO, emit,join_room,leave_room
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_FILE_DIR"]="/tmp/flask-session"
Session(app)
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
                    "passwords":{},
                    "short_name":{}
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
This dictionary contains the usernames and their sessions.
"""
user_sessions = {}
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

sids_users={}

def private_channels_info(rooms_list):
	#private_channels.items()
	private_info={}
	tmp={}
	for room in rooms_list:
		tmp[room]={}
		tmp[room]['name']=private_channels['names'][room]
		tmp[room]['password']=private_channels["passwords"][room]
		#private_info.append(tmp)

	return tmp #private_info

def update_room_msg(data,room):
	msg = {'text': data['msg'], 'username': data['username'], 'time': time.time()*1000}
	if channels_msgs[room]['num_msgs'] >= 50:
		channels_msgs[room]['msgs'].pop(0)
	else:
		channels_msgs[room]['num_msgs'] += 1
	channels_msgs[room]["msgs"].append(msg)
	return msg

@app.route("/")
def index():
	#session.clear()
	if session.get('uid') is None:
		import uuid
		session['uid']=str(uuid.uuid4())
	else:
		pass
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
	cur_channel=data.get('channel')
	username=data.get('username')

	if session['uid'] != user_sessions.get(username):
		emit("user_exists",{"error":"Username already tied to a session."})
		return
	if cur_channel is None:
		channel=channels_list[0]
	else:
		channel=cur_channel
	join_room(channel)
	print("reconnect")
	emit("update_users",{"users":list(users.keys())})
	username=data['username']
	#remove_old_usersid(username)
	users[username]=request.sid

	sids_users[request.sid]=username
	private_rooms=users_rooms.get(username)
	if private_rooms:
		full_names=private_rooms
		#private_rooms['full_names']=private_rooms
		private_rooms=private_channels_info(private_rooms)
		private_rooms['full_names']=full_names
	else:
		private_rooms={}

	emit("update_users",{'users':list(users.keys())})
	emit("update_channels",{"channels":channels_list,"private_channels":private_rooms},room=request.sid)
	emit("joined",{"success":True,"channel_msgs":channels_msgs[channel]['msgs']},room=request.sid)

@socket.on("join")
def join(data):
	if data == "":
		emit("joined",{success:False, channel:"", "password":"","error":"Response was not received","channel_msgs":""},
		     room=request.sid)
	password=data.get('password')
	room = data["channel"]
	print(data)
	username =data['username']
	# print("password",password)
	if room not in channels_list and room not in private_channels['names']:
		# print('not channels')
		# print(private_channels['short_name'])
		# print(room)
		# print(room not in private_channels['short_name'])
		if room not in private_channels['short_name'] is True:
			emit("joined",{'success':False, "password":password, "channel":room,
			               "error":"Invalid room selected.","channel_msgs":""},room=request.sid)
			return
		else:
			if private_channels['short_name'].get(room):
				full_names=private_channels['short_name'][room]
			else:
				emit("joined", {'success': False, "password": password, "channel": room,
				                "error": "Invalid room selected.", "channel_msgs": ""}, room=request.sid)
				return

			i=0
			for i,name in enumerate(full_names):
				if data["password"] == private_channels["passwords"][name]:
					room=name
					break
			else:
				emit("joined", {'success': False, "channel":room, "password":password, "error": "Invalid password provided.",
				                "channel_msgs": ""}, room=request.sid)
				return
			msg= {"error":"",'channel': data["channel"], 'full_name': room, 'password': data['password'],
			      'msg': f"Channel {data['channel']} created with password {password}"}
			if not users_rooms.get(username):
				users_rooms[username] = []
				users_rooms[username].append(room)

			join_room(room)
			emit("private_channel", msg, room=request.sid)
			return


	join_room(room)

	emit("joined",{"success":True,"channel":room,"channel_msgs":channels_msgs[room]['msgs']},room=request.sid)

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
	#print(data)
	msg=update_room_msg(data,room)
	#emit("announce_room",{"channel_msgs":channels_msgs[room]['msgs']},room=room)
	emit("announce_room",{"msg":msg},room=room,broadcast=True)

@socket.on("rejoin_general")
def rejoin_general():
	emit("announce_to_main",{"channel_msgs":channels_msgs['main']['msgs']},broadcast=True)
	
@socket.on("create_channel")
def create_channel(data):
	error_str=""
	channel=data["channel"]
	print("channel_name",channel)
	if channel == "" or channel is None:
		error_str="No data received"
	elif channel in channels_list or channel in private_channels:
		error_str="Channel cannot already exist"
	else:
		channels_list.append(channel)

		channels_msgs[channel]={'num_msgs':0,'msgs':[]}
	if error_str != "":
		emit("add_channel",{"channel":channel,"error":error_str},room=request.sid)
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
		session['username']=username
		user_sessions[username] = session['uid']
		users_rooms['username']=[]

	if error == "":
		emit('add_user',{'username':username,'error':''},broadcast=True)
	else:
		emit('add_user',{'username':username,'error':error},room=request.sid)

@socket.on("create_private_channel")
def create_private_channel(data):
	channel_name=data.get('channel')
	# print(channel_name)
	# print(request.sid)
	# print(session['uid'])
	username=data.get('username')
	full_name=channel_name+session['uid'][0:4]
	password=data.get('password')
	msg={"msg":"","error":""}
	if channel_name is None or channel_name == "":
		msg["error"]="No channel name given."
	elif channel_name in channels_list:
		msg["error"] = "Channel name must be unique and not mirror any of the generals."
	elif full_name in private_channels["names"]:
		msg["error"] = "Error your channel name must be unique."
	else:
		if private_channels['short_name'].get('channel_name'):
			private_channels['short_name'][channel_name].append(full_name)
		else:
			private_channels['short_name'][channel_name]=[full_name]

		private_channels["names"][full_name]=channel_name
		private_channels["passwords"][full_name]=password
		socket.server.enter_room(request.sid,full_name)
		msg['channel']=channel_name
		msg['full_name']=full_name
		msg['password']=password
		msg['msg']=f"Channel {channel_name} created with password {password}"
		if not users_rooms.get(username):
			users_rooms[username]=[]
		users_rooms[username].append(full_name)
	# print(private_channels)

	channels_msgs[full_name] = {'num_msgs': 0, 'msgs': []}
	emit("private_channel",msg,room=request.sid)

@socket.on('create_pm_room')
def create_pm_room(data):
	print('create_pm')
	# print(data)
	# print(users)
	sender=data.get('username')
	receiver=data.get('to_user')
	# print(receiver not in users)
	if receiver not in users:
		# print("not in users")
		emit("add_pm", {'error': 'User not found', 'msg': ''}, room=request.sid)
	else:
		room = users[receiver] + users[sender]
		user_pms[room]=[sender,receiver]
		channels_msgs[room]={'msgs':[],'num_msgs':0}
		socket.server.enter_room(users[receiver], room)
		socket.server.enter_room(request.sid, room)
		# message = {'text': data['msg'], 'sender': sender, 'time': data['time'],'error':''}
		msg=update_room_msg(data,room)
		message = {'room_name': room, 'from': sender, 'to': receiver,'msg':msg,'error':''}
		emit("add_pm",message,room=room,broadcast=True)

@socket.on("send_pm")
def private_msg(data):
	# print(data)
	sender=data.get('username')
	receiver=data.get('to_user')
	room=data.get('room')
	if room not in user_pms:
		# print('user_pms',user_pms)
		emit("pm",{"error":"The room doesn't exist.","msg":""})
	if receiver not in users:
		# print('err')
		emit("pm",{'error':'User not found','msg':''},room=request.sid)
	else:
		msg = update_room_msg(data, room)
		# print("sent")
		message = {"error":"",'room_name': room, 'from': sender, 'to': receiver, 'msg': msg}
		emit("pm",message,room=room)

@socket.on("get_pms")
def get_pms(data):
	pass

@socket.on("update_user_channels")
def update_user_channels(data):
	pass
@socket.on("disconnect")
def disconnect():
	print('disconnected')
	print(request.sid)
	print(sids_users)
	if sids_users.get(request.sid):
		print(sids_users[request.sid])
		target_username=sids_users[request.sid]
		sid_local=dict(sids_users)
		pop_list=[]
		for sid, username in sid_local.items():
			if username == target_username:
				pop_list.append(sid)

		for pop in pop_list:
			sids_users.pop(pop)

		emit('user_left',{'username':target_username})

@socket.on("client_disconnect")
def client_disconnect(data):
	username=data.get('username')
	if username is not None:
		emit("user_left",{'username':username})
	pass