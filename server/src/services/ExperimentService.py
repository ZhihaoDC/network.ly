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


def delete_by_id(model, id):
    deleted_id = model.query.filter_by(experiment_id=id).delete()
    commit_changes()
    return id


# def edit_instance(model, id, **kwargs):
#     instance = model.query.filter_by(id=id).all()[0]
#     for attr, new_value in kwargs.items():
#         setattr(instance, attr, new_value)
#     commit_changes()


def commit_changes():
    db.session.commit()