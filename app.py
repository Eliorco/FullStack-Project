from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy
import jwt

# ### setup ### #
app = Flask(__name__)
app.config.from_object(__name__)
# I'll never add secret keys and passwords to github, only for assignment POC
app.secret_key = "$2b$12$O6de.w1FB5HTnee8Ak9WLusDlGoouoVT5CCQMGEwTMfD6nUI/BUiC"
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///message_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
CORS(app)

# ### models ### #
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    messages = db.relationship('Message', backref='owner', lazy=True)

    def __repr__(self):
        return f'User({self.first_name}, {self.email}, {self.id})'


class Message(db.Model):
    msg_id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    message_body = db.Column(db.Text, nullable=False)
    creation_date = db.Column(db.String(50), nullable=False, default=datetime.utcnow)

    def to_dict(self):
        return dict(
            msg_id=self.msg_id,
            sender=full_name_by_uid(self.sender),
            receiver=full_name_by_uid(self.receiver),
            title=self.title,
            message_body=self.message_body,
            creation_date=self.creation_date
        )

    def __repr__(self):
        return f"Message('{self.title}', '{self.msg_id}', '{self.receiver}')"

# ### utils ### #
response_template = {
    'status': '',
    'msg': ''
}


def full_name_by_uid(id):
    usr = User.query.filter_by(id=id).first()
    if usr:
        return f'{usr.first_name} {usr.last_name}'


def uid_by_name(first_name, last_name):
    usr = User.query.filter_by(first_name=first_name, last_name=last_name).first()
    if usr:
        return usr.id
    print(f"no user named {first_name} {last_name} found, creating and insert into db")
    u = User(email=f'{first_name}{last_name}@gmail.com', first_name=first_name, last_name=last_name, password='blabla123')
    db.session.add(u)
    db.session.commit()
    return u.id


def get_uid_from_token():
    try:
        token = request.headers.get('Authorization').split(" ")[1]
        if token:
            return jwt.decode(token, app.config['SECRET_KEY']).get('uid')
    except Exception as e:
        print(e)

# ### route ### #
@app.route("/")
def home():
    return '<H1>Herolo World<H1/>'


@app.route("/api/")
def api():
    return jsonify({"msg": "hello from flask"})


@app.route("/api/write_message", methods=['POST'])
def write_message():
    response_template['msg'] = "write message from flask"
    if request.method == 'POST' and request.json:
        try:
            id = get_uid_from_token()
            if not id:
                return jsonify({"msg": "NOT AUTHORIZED"})
            new_message = request.json
            full_name = new_message.get('receiver')
            first, last = full_name[:full_name.find(' ')], full_name[full_name.find(' ')+1:]
            rec = uid_by_name(first, last)
            msg = Message(sender=id, receiver=rec, title=new_message.get('title'), message_body=new_message.get('message_body'))
            db.session.add(msg)
            db.session.commit()

            response_template['status'] = 'OK'
            response_template['msg'] = 'Message added'
        except Exception as e:
            print(e)

    return jsonify(response_template)


@app.route("/api/get_all")
def get_all():
    id = get_uid_from_token()
    if not id:
        return jsonify({"msg": "NOT AUTHORIZED"})
    user_sent_messages = User.query.filter_by(id=id).first().messages
    user_rec_messages = Message.query.filter_by(receiver=id)
    all_messages = list([u_msg.to_dict() for u_msg in user_sent_messages] + [u_msg.to_dict() for u_msg in user_rec_messages])
    return jsonify({
        'msg': "get all from flask",
        'messages': all_messages
    })


@app.route("/api/delete_message/<int:message_id>", methods=['DELETE'])
def delete_message(message_id):
    response_template['msg'] = 'Message not found in db'
    msg = Message.query.filter_by(msg_id=message_id)
    if msg:
        msg.delete()
        db.session.commit()
        response_template['msg'] = "Deleted from db"
        response_template['status'] = 'OK'

    return jsonify(response_template)


@app.route("/login",  methods=['POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = User.query.filter_by(email=email, password=password).first()
            if user:
                token = jwt.encode({
                    'uid': user.id,
                    'iat': datetime.utcnow(),
                    'exp': datetime.utcnow() + timedelta(minutes=30)},
                    app.config['SECRET_KEY'])
                return jsonify({'token': token.decode('UTF-8')})
    return jsonify({'message': 'Invalid credentials', 'authenticated': False}), 401


@app.route("/signup",  methods=['POST'])
def signup():
    if request.method == 'POST':
        data = request.get_json()
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        password = data.get('password')
        email = data.get('email')

        if first_name and last_name and password:
            if not email:
                email = f'{first_name}{last_name}@gmail.com'
            u = User(email=email, first_name=first_name, last_name=last_name, password=password)
            db.session.add(u)
            db.session.commit()
            return jsonify({'msg': f'User named {first_name} {last_name} was added successfully'})
    return jsonify({'msg': 'Failed to add user'})


if __name__ == "__main__":
    app.run(debug=True)

