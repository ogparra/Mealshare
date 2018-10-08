# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------

def get_items():
    """This controller is used to get the posts.  Follow what we did in lecture 10, to ensure
    that the first time, we get 4 posts max, and each time the "load more" button is pressed,
    we load at most 4 more posts."""
    # Implement me!
    start_idx = int(request.vars.start_idx) if request.vars.start_idx is not None else 0
    end_idx = int(request.vars.end_idx) if request.vars.end_idx is not None else 0
    # We just generate a lot of of data.
    items = []
    b_posts = []
    has_more = False
    rows = db().select(db.item.ALL, orderby=~db.item.id, limitby=(start_idx, end_idx + 1))
    if auth.user_id is None: return

    for i, r in enumerate(rows):
        if i < end_idx - start_idx:
            if(r.user_email == auth.user.email):
                r.check_user = True
            else:
                r.check_user = False

            if(r.created_on == r.updated_on): 
                r.updated_on = "";
            p = dict(
                id = r.id,
                item_name = r.item_name,
                exp_date = r.exp_date,
                item_num = r.item_num,
                check_user = r.check_user,
                email = r.user_email
            )
            items.append(p)
        else:
            has_more = True
    logged_in = auth.user_id is not None

    return response.json(dict(  
        items=items,
        logged_in=logged_in,
        has_more=has_more,
    ))


def get_items_for_user():
    """This controller is used to get the posts.  Follow what we did in lecture 10, to ensure
    that the first time, we get 4 posts max, and each time the "load more" button is pressed,
    we load at most 4 more posts."""
    # Implement me!
    useremail = request.vars.useremail
    # We just generate a lot of of data.
    user_items = []
    rows = db().select(db.item.ALL, orderby=~db.item.id)
    if auth.user_id is None: return
    for i, r in enumerate(rows):
            if(useremail != r.user_email):
                continue

            if (r.created_on == r.updated_on):
                r.updated_on = "";
            p = dict(
                id=r.id,
                item_name=r.item_name,
                exp_date=r.exp_date,
                item_num=r.item_num,
                check_user=r.check_user,
                email = r.user_email
            )
            user_items.append(p)
    return response.json(dict(
        user_items=user_items,
    ))

def get_logged():
    if auth.user_id is None: return
    logged_user = auth.user.email
    return response.json(dict(
        logged_in = logged_user
    ))


def get_users():
    print ("hello")
    reg_users = []
    user_logged_in = None
    user1 = None
    rows = db().select(db.auth_user.ALL, orderby=db.auth_user.last_name)
    if auth.user_id is None: return
    for row in rows:
        if(row.email == auth.user.email):
            user_logged_in = row.email
            print(row.email)
            user1 = get_user_name_from_email(user_logged_in)
            print(user1)
            continue
        
        u = dict(
            id = row.id,
            fname = row.first_name,
            lname = row.last_name,
            email = row.email,
            image = row.image,
        )
        reg_users.append(u)
    print(user1)
    return response.json(dict(reg_users = reg_users, user= user_logged_in, user_n = user1 ))


def add_grocery_item():

    item_id = db.item.insert(
        item_name = request.vars.item_name,
        exp_date = request.vars.exp_date,
        item_num = request.vars.num_items,
    )
    i = db.item(item_id)
    return response.json(dict(item = i))


def get_user_name_from_email(email):
    """Returns a string corresponding to the user first and last names,
    given the user email."""
    u = db(db.auth_user.email == email).select().first()
    if u is None:
        return 'None'
    else:
        return ' '.join([u.first_name, u.last_name])


#@auth.requires_signature()
def del_grocery_item():
    """Used to delete a post."""
    # Implement me!
    db(db.item.id == request.vars.item_id).delete()
    return "ok"

#@auth.requires_signature()
def edit_grocery_item():
    edited_item = db.item(request.vars.item_id)
    edited_item.updated_on = datetime.datetime.utcnow()
    name = request.vars.item_name
    exp_d = request.vars.exp_date
    item_num = request.vars.item_num
    edited_item.update_record(item_name = name)
    edited_item.update_record(exp_date = exp_d)
    edited_item.update_record(item_num = item_num)
    return response.json(dict(edit_item = edited_item))

def create_meal(): 
    import random

    a = request.vars.item_fuser
    b = request.vars.item_name
    c = request.vars.item_quan
    d = request.vars.item_exp
    f = request.vars.item_date
    #print(type(e))

    e = request.vars.item_ident
    g = request.vars.item_owner
    db.meal.insert(
          friend_email = a,
          item_name = b,
          item_num = c ,
          item_exp = d,
          identifier = e,
          created_on = f,
          item_owner = g
        )

    return "ok"

def get_meals():
    meals = []
    rows = db().select(db.meal.ALL)
    if auth.user_id is None: return
    for row in rows:
        if (row.friend_email != auth.user.email):
            continue
        m = dict(
            is_confirmed = row.is_confirmed,
            req_owner = row.user_email,
            item_owner = row.item_owner,
            identifier = row.identifier,
            created_on = row.created_on,
            item_name = row.item_name,
            item_exp = row.item_exp,
            item_num = row.item_num
            )
        meals.append(m)
    return response.json(dict(meals = meals))

def index():
    """
    This is your main controller.
    """
    # I am creating a bogus list here, just to have some divs appear in the
    # view.  You need to read at most 20 posts from the database, in order of
    # most recent first, and you need to return that list here.
    # Note that posts is NOT a list of strings in your actual code; it is
    # what you f from a db(...).select(...).
    posts = ['banana', 'pear', 'eggplant']
    return dict()


@auth.requires_login()
def edit():
    """
    This is the page to create / edit / delete a post.
    """
    return dict()


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


