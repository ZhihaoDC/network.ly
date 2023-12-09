from src import db

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