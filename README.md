# MessengerSocket
A chat socket created with rooms, you can create isolated temporary rooms ( and history ).</br>
Developmented with Flask and Flask-SocketIO, to render front-end i using jinja ( backend render ).

#### Structure of Project

    ├── LICENSE 
    ├── main.py  --- server side code
    ├── poetry.lock   --- dependences
    ├── pyproject.toml  --- dependences
    ├── README.md 
    ├── static  --- static files to jinja
    │   └── css
    │       └── style.css
    └── templates  --- templates of views
        ├── base.html
        ├── home.html
        └── room.html



## Thanks 
<a href="https://www.youtube.com/@TechWithTim">@TechWithTim</a> for recorded videos about how work a chat socket.</br>
<a href="https://flask-socketio.readthedocs.io/en/latest/">All Contributions</a> from FlaskSocketIO project.
