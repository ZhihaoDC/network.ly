from src import db


def get_by_id(model, user_id, id):
    dataset = model.query.filter_by(user_id=user_id, id=id).first()
    if dataset:
        return dataset.serialized
    return dataset

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
    dataset_to_delete = model.query.filter_by(user_id=user_id, id=id).first()
    db.session.delete(dataset_to_delete)
    commit_changes()    
    return dataset_to_delete.serialized


def commit_changes():
    db.session.commit()