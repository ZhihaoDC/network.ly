
from src import db

class Dataset(db.Model):
    __tablename__ = 'DATASET'
    __table_args__ = {'extend_existing': True}

    id = db.Column(
        db.String(32),
        primary_key=True
    )  

    creation_date = db.Column(
        db.DateTime, 
        default=db.func.current_timestamp()
    )

    name = db.Column(
        db.String(50)
    )
    
    json = db.Column(
        db.JSON, 
        nullable=False
    )
    
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("USER.id"),
        nullable=False
    )

    experiments = db.relationship('Experiment', backref='DATASET', cascade="all, delete-orphan")

    @property
    def serialized(self):
        """Return object data in serializeable format"""

        return {
            'id': self.id,
            'creation_date': self.creation_date.strftime("%Y/%m/%d, %H:%M"),
            'name': self.name,
            'json': self.json,
            'user_id': self.user_id
        }