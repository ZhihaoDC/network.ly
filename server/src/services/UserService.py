from src import db


def get_by_email(model, email):
    user = model.query.filter_by(email=email).first()
    if user:
        return user.serialized
    return user

def get_by_username(model, username):
    user = model.query.filter_by(username=username).first()
    if user:
        return user.serialized
    return user

def add_instance(model, **kwargs):
    instance = model(**kwargs)
    instance = db.session.merge(instance)
    commit_changes()
    return instance.serialized

def delete_by_id(model, user_id):
    user_to_delete = model.query.filter_by(id=user_id).first()
    db.session.delete(user_to_delete)
    commit_changes()    
    return user_to_delete.serialized

def commit_changes():
    db.session.commit()