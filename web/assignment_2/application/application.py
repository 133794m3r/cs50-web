import os

from flask import Flask,jsonify,request
import time,json
from flask_socketio import SocketIO, emit,join_room,leave_room

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socket = SocketIO(app)

channels_list = ["main"]
"""
User Private messages.

It's a dictionary that looks like this.
user_pms[<username>] = { num_msgs:<number of messages>,
						 msgs:[<list>,<of>,<msgs>]
						}
"""
user_pms = {}

"""
Users dictionary
It basically looks like this. Where request.sid is the socketio session id.
users[<username>] = request.sid
"""
users = {}
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
	emit("get channels",{"channels":channels})

@socket.on("join")
def join(data):
	if data is "":
		send("joined",{success:False,"error":"Response was no received","channel_msgs":""},room=request.sid)
	room = data["channel"]
	if room not in channels_list:
		send("joined",{success:False,"error":"Invalid room selected.","channel_msgs":""},room=request.sid)
	join_room(room)

	if channels_msgs["main"]["num_msgs"] >= 50:
		channel_msgs["main"]["msgs"].pop(0)
	else:
		channel_msgs["main"]["num_msgs"]+=1
	msg = {'text':data['msg'],'username':data['username'],"time":data["time"]}
	channel_msgs["main"]["msgs"].append(msg)
	emit("joined",{"success":True,"channel_msgs":channel_msgs[channel]},room=room)

@socket.on("send_to_main")
def submit_to_all(data):
	msg = {'text':data['msg'],'username':data['username'],"time":data["time"]}
	if channels_msgs["main"]["num_msgs"] >= 50:
		channel_msgs["main"]["msgs"].pop(0)
	else:
		channel_msgs["main"]["num_msgs"]+=1

	channel_msgs["main"]["msgs"].append(msg)
	emit("send_to_main",{"channel_msgs":channels_msgs},broadcast=True)

@socket.on("rejoin_general")
def rejoin_general():
	emit("announce_to_main",{"channel_msgs":channels_msgs},broadcast=True)
	
@socket.on("create_channel")
def create_channel(data):
	error_str=""
	channel=data["channel"]
	if channel == "" or channel is None:
		error_str="No data received"
	elif channel in channels_list:
		error_str="Channel cannot already exist"
	else:
		channels_list.append(channel)
		channels_msgs[channel]={'num_msgs':0,msgs:[]}
	if error_str != "":
		send("add_channel",{"channel":channel,"error":error_str},room=request.sid)
	else:
		emit("add_channel",{"channel":channel},broadcast=True)


@socket.on("update_user_channels")
def pass1():
	pass
		
