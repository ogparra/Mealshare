# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.

import datetime

db.define_table('item',
                Field('user_email', default=auth.user.email if auth.user_id else None),
                Field('item_content', 'text'),
                Field('item_name', 'text', default= None),
                Field('created_on', 'datetime', default=datetime.datetime.utcnow()),
                Field('updated_on', 'datetime', update=datetime.datetime.utcnow()),
                Field('exp_date', 'text', default=None),
				Field('item_num', 'integer', default = 1),
                Field('check_user', default = False)
                )

db.define_table('friends',
                Field('user_email', default=auth.user.email if auth.user_id else None),
                Field('friend_email', 'text'),
                Field('is_mutual', 'boolean', default = False),
                Field('added_on', 'datetime', default=datetime.datetime.utcnow())
                )

# table for meal sharing
db.define_table('meal',
                Field('user_email', default=auth.user.email if auth.user_id else None), 
                Field('friend_email', 'text' ), 
                Field('is_confirmed', 'boolean', default= False ),
                Field('created_on', 'string'),
                Field('item_name', 'text' ),
                Field('item_num', 'text' ),
                Field('item_exp', 'text' ), 
                Field('identifier', 'double'),
                Field('item_owner', 'text')
                )

#meal table with specific fields

# I don't want to display the user email by default in all forms.
# db.post.user_email.readable = db.post.user_email.writable = False
# db.post.item_content.requires = IS_NOT_EMPTY()
# db.post.created_on.readable = db.post.created_on.writable = False
# db.post.updated_on.readable = db.post.updated_on.writable = False
#db.post.user_email.readable = db.post.user_email.writable = False
#db.post.post_content.requires = IS_NOT_EMPTY()
#db.post.created_on.readable = db.post.created_on.writable = False
#db.post.updated_on.readable = db.post.updated_on.writable = False

# after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)
