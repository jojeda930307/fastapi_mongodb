import src.config.database as db


def update_tags(ref, new_tag):
    db.mydb.users.update_one({'_id': ref}, {'$push': {'address': new_tag}})