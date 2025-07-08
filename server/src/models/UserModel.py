from src import db


class User(db.Model):
    __tablename__ = 'USER'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(256), nullable=False)
    firstname = db.Column(db.String(50))
    lastname = db.Column(db.String(100))
    profile_description = db.Column(db.String(250))

    
    datasets = db.relationship('Dataset', backref='User', cascade="all, delete-orphan")
    experiments = db.relationship('Experiment', backref='User', cascade="all, delete-orphan")

    @property
    def serialized(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "profile_description": self.profile_description
        }