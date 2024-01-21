import random 
from string import ascii_uppercase
from flask_socketio import join_room, send, leave_room, SocketIO
from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.config["SECRET_KEY"] = "AverySecurityPassword"

socketio = SocketIO(app)


rooms = {}

def generate_unique_code( lenght ):
    while True:
        code = ""
        for _ in range(lenght):
            code += random.choice(ascii_uppercase)

        if code not in rooms:
            break

    return code

@app.route("/", methods=["GET", "POST"])
def home():
    session.clear()

    if request.method == "POST":
        # takes variables from form 
        name = request.form.get("name")
        code = request.form.get("code")
        join = request.form.get("join", False)
        create = request.form.get("create", False)

        if not name:
            return render_template("home.html", error="Please enter a name.", code=code, name=name)

        if join and not code:
            return render_template("home.html", error="Please enter a room code.", code=code, name=name)

        # check if exist a room if not create 
        room = code
        if create != False:
            # enter in a room 
            room = generate_unique_code(4)
            # save this in a db
            rooms[room] = {"members" : 0, "messages": []}

        elif code not in rooms:
            return render_template("home.html")

        session["room"] = room
        session["name"] = name
        return redirect(url_for("room"))

    return render_template("home.html")

@app.route("/room")
def room():

    room = session.get("room", None)

    if room is None or room not in rooms:
        return redirect(url_for("home", error="Room does not exist"))

    return render_template("room.html")

@socketio.on("connect")
def connect( auth ):
    room = session.get('room', None)
    name = session.get('name', None)
    
    if not room and not name:
        return 
    if room not in rooms:
        leave_room(room)
        return
    
    join_room(room)
    send({"name" : name, "message": "has entered the room"}, to=room) # send a json to room
    rooms[room]["members"] += 1
    print(f"{name} joined room {room}")


@socketio.on("disconnect")
def disconnect():
    room = session.get("room")
    name = session.get("name")

    leave_room(room)

    if room in rooms:
        rooms[room]["members"] -= 1
        if rooms[room]["members"] <= 0:
            del rooms[room]

    send({"name" : name, "message": "has lefft the room"}, to=room)
    print(f"{name} has left the room {room}")

@socketio.on("message")
def message( data ):

    room = session.get("room")
    if room not in rooms:
        return 

    content = {
        "name" : session.get("name"),
        "message" : data["data"],
    }

    send( content, to=room )
    rooms[room]['messages'].append( content )
    print(f"{session.get("name")} said : {data['data']}")

if __name__ == "__main__":
    socketio.run(app, debug=True, host="0.0.0.0")