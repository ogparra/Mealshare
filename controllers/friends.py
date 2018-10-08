import datetime

def get_user_name_from_email(email):
    """Returns a string corresponding to the user first and last names,
    given the user email."""
    u = db(db.auth_user.email == email).select().first()
    if u is None:
        return 'None'
    else:
        return ' '.join([u.first_name, u.last_name])


def add_friend():
    email = request.vars.useremail
    # check to see if user has already request other user
    rows = db().select(db.friends.ALL)
    state = True

    for r in rows:
        if( ((r.user_email == auth.user.email) and (r.friend_email == email)) or
            (r.friend_email == auth.user.email) and (r.user_email == email) ):
            state = False

    if(state):
        friend_id = db.friends.insert(
            user_email = auth.user.email,
            friend_email = email,

        )

    return response.json(dict(res="insert"))

def get_friends():
    if auth.user_id is None: return
    friends = []
    f = None 
    user_name1= ""
    pend_req = None 
    # rows = db().select(db.friends.user_email==auth.user.email or db.friends.friend_email==auth.user.email)
    rows = db().select(db.friends.ALL)
    for r in rows:

        if(r.user_email == auth.user.email or r.friend_email == auth.user.email):
            if (r.user_email == auth.user.email):
                f_email = r.friend_email
                user_name1 = get_user_name_from_email(r.friend_email)
                pend_req = False
            elif(r.friend_email == auth.user.email):
                f_email = r.user_email
                user_name1 = get_user_name_from_email(r.user_email)
                pend_req = True

            f = dict(
                id = r.id,
                friend_email = f_email,
                added_on = datetime.datetime.utcnow(),
                is_mutual = r.is_mutual,
                user_name = user_name1,
                request = pend_req,
            )

            friends.append(f)
    return response.json(dict(friends = friends, request = pend_req))

def confirm_request():
    email = request.vars.useremail
    f_request = db.friends(request.vars.id)
    f_request.update_record(is_mutual=True)
    return "ok"

def del_friend():
    """Used to delete a friend"""
    # Implement me!
    print(request.vars.friend_id)
    db(db.friends.id == request.vars.friend_id).delete()
    db.commit()
    return "ok"