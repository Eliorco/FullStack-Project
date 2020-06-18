<h1>Messaging Web Application</h1>
<br>
<h2>Full Stack Assignment using Flask as backend and Vue as frontend</h2>
<br>
This is a basic CRUD Fullstack assignment that simply serve both ends and dealing requests front=Vue, and API calls=Flask.
<br>
The App supports CRUD functions and user authentication methods(login, logout, signup(only by curl request to flask))
In order to use this repo, clone the code and delete all unecessary deployment files, and you ready to go!
<br><br>
NOTE: in order to register user, use this example to send a curl request:
<code>
curl -X POST -H "Content-Type: application/json" -d '{"first_name": "Chiko", "last_name":"Vediko", "password": "blublu123"}' http://localhost:5000/signup</code>
create this request only for local flask server, Vue won't answer to that.
