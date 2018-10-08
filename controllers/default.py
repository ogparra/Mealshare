# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------



def index():
    """
    This is your main controller.
    """
    # I am creating a bogus list here, just to have some divs appear in the
    # view.  You need to read at most 20 posts from the database, in order of
    # most recent first, and you need to return that list here.
    # Note that posts is NOT a list of strings in your actual code; it is
    # what you get from a db(...).select(...).
    #auth = db().select(db.auth_user.ALL)
    #for row in auth:
    #    print (row.first_name)
    posts=[]
    return dict(posts=posts)


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
    #form=FORM('Your name:',
    #          INPUT(_name='name', requires=IS_NOT_EMPTY()),
    #         INPUT(_type='submit'))

    return dict(form=auth())

def profile():

    return dict(form= auth.profile())


def get_profile():
    print ("hello")
    print(type(int(request.vars.id)))
    profile = None
    rows = db().select(db.auth_user.ALL)
    if auth.user_id is None: return
    for row in rows:
        print(type(row.id))
        if(row.id != int(request.vars.id)):
            continue  

        print("hi");
        u = dict(
            id = row.id,
            fname = row.first_name,
            lname = row.last_name,
            email = row.email,
            image = row.image,
            bio = row.bio
        )

        return response.json(dict(user = u))


def create_meal():


    return dict()

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


