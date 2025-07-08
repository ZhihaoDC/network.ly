from src import db


def get_all(model):
    data = model.query.all()
    return data


def get_all_by_user_id(model, user_id):
    data = model.query.filter_by(user_id=user_id).order_by(model.creation_date).all()
    return [result.serialized for result in data]


def add_instance(model, **kwargs):
    instance = model(**kwargs)
    instance = db.session.merge(instance)
    commit_changes()
    return instance.serialized


def delete_by_id(model, user_id, id):
    experiment_to_delete = model.query.filter_by(user_id=user_id, experiment_id=id).first()
    db.session.delete(experiment_to_delete)
    commit_changes()    
    return experiment_to_delete.serialized


def commit_changes():
    db.session.commit()