import random 
from string import ascii_uppercase
from flask_socketio import join_room, send, leave_room, SocketIO
from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.config["SECRET"] = "AverySecurityPassword"

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
        
        if join != False and not code:
            return render_template("home.html", error="Please enter a room code.", code=code, name=name)
        
        # check if exist a room if not create 
        room = code
        if create:
            # enter in a room 
            room = generate_unique_code(4)
            # save this in a db
            rooms[room] = {"members" : 0, "messages": []}
        
        elif code not in rooms:
            return render_template("home.html", error="Room does not exist.", code=code, name=name)

        session["room"] = room
        session["name"] = name
        return redirect(url_for("room"))

    return render_template("home.html")

@app.route("/room")
def room():
    
    room = session.get("room", None)

    if room is None or room not in rooms:
        return redirect(url_for("home.html", error="Room does not exist"))

    
    return render_template("room.html")


if __name__ == "__main__":
    socketio.run(app, debug=True)