from app import db, User, Message

Users = [
    {
        'first_name': 'Elior',
        'last_name': 'Cohen',
        'email': 'eliorc1988@gmail.com',
        'password': 'blabla123'
    },
    {
        'first_name': 'Donald',
        'last_name': 'Trump',
        'email': 'dt@usa.gov',
        'password': 'blabla123'
    },
    {
        'first_name': 'Moshe',
        'last_name': 'Rabenu',
        'email': 'pigent@gmail.com',
        'password': 'blabla123'
    },
    {
        'first_name': 'Benjamin',
        'last_name': 'Netanyahu',
        'email': 'bibi@gov.il',
        'password': 'blabla123'
    }
]

Messages = [
    {
        'sender': 'John Doh',
        'receiver': 'Moshe Rabenu',
        'title': 'Job Application',
        'message_body': 'Natural born leader',
        'creation_date': '27/05/2020 21:37:05'
    },
    {
        'sender': 'Moshe Rabenu',
        'receiver': 'John Doh',
        'title': 'Your Hired!',
        'message_body': 'Seems you got everything for this job',
        'creation_date': '28/05/2020 09:30:44'
    },
    {
        'sender': 'Donald Trump',
        'receiver': 'Benjamin Netanyahu',
        'title': 'Confidential',
        'message_body': 'WHAZAAAAAAAP',
        'creation_date': '27/05/2020 10:09:14'
    },
    {
        'sender': 'Benjamin Netanyahu',
        'receiver': 'Donald Trump',
        'title': 'Re: Confidential',
        'message_body': 'Donald is that you?',
        'creation_date': '27/05/2020 16:40:00'
    },
    {
        'sender': 'Donald Trump',
        'receiver': 'Benjamin Netanyahu',
        'title': 'Re: Re: Confidential',
        'message_body': 'WHAZzzzzzzzzzzzAAAAAAaaaaaaaaaaaAppppppppP',
        'creation_date': '27/05/2020 17:26:23'
    }
]


def uid_by_name(first_name, last_name):
    usr = User.query.filter_by(first_name=first_name, last_name=last_name).first()
    if usr:
        return usr.id
    print(f"no user named {first_name} {last_name} found, creating and insert into db")
    u = User(email=f'{first_name}{last_name}@gmail.com', first_name=first_name, last_name=last_name, password='blabla123')
    db.session.add(u)
    db.session.commit()
    return u.id


if __name__ == "__main__":
    db.drop_all()
    db.create_all()

    for u in Users:
        db.session.add(User(first_name=u.get('first_name'), last_name=u.get('last_name'), email=u.get('email'), password=u.get('password')))

    db.session.commit()

    for m in Messages:
        f_sender, l_sender = m.get('sender').split(" ")
        uid_sender = uid_by_name(f_sender, l_sender)

        f_receiver, l_receiver = m.get('receiver').split(" ")
        rec_uid = uid_by_name(f_receiver, l_receiver)

        db.session.add(Message(sender=uid_sender, receiver=rec_uid, title=m.get('title'), message_body=m.get('message_body')))

    db.session.commit()