
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash

from sqlalchemy.exc import OperationalError
import time
import json
import hashlib

from . import app_config
from src.plugins.SQLAlchemy import db
from src.api.UserController import UserController
from src.api.ExperimentController import ExperimentController
from src.api.DatasetController import DatasetController
from src.api.LouvainController import LouvainController
from src.api.GirvanNewmanController import GirvanNewmanController
from src.api.GraphVisualizationController import GraphVisualizationController
from src.models.UserModel import User
from src.models.DatasetModel import Dataset
from src.services import UserService, DatasetService
import src.api.__network_formatter__ as nw_formatter
############################################## APP #################################################





def create_app(env="PROD"):
    app = Flask(__name__)
    app.config.from_object(__name__)

    # Register controller routes
    app.register_blueprint(LouvainController)
    app.register_blueprint(GirvanNewmanController)
    app.register_blueprint(GraphVisualizationController)
    app.register_blueprint(ExperimentController)
    app.register_blueprint(DatasetController)
    app.register_blueprint(UserController)

    # Database config
    app.config['SQLALCHEMY_DATABASE_URI'] = app_config.DATABASE_CONNECTION_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.app_context().push()

    if env != 'TEST':
        # Start app and database
        db.init_app(app)
        

        #Retry on connection failure
        MAX_RETRIES = 10
        TIME_RETRY_SECS = 5
        retry_count = MAX_RETRIES
        is_db_connected = False
        while retry_count >= 0 and not is_db_connected:
            try:
                db.create_all()
                is_db_connected = True
            except OperationalError:
                print(f"Attempting to reconnect to database... (Retry again in {TIME_RETRY_SECS} seconds...)")
                time.sleep(TIME_RETRY_SECS)
                if retry_count == 0:
                    print(f"Connection failed. (Tried to reconnect {MAX_RETRIES} times")
        
        init_database()

    # enable CORS
    CORS(app, resources={r'/*': {'origins': '*'}})

    return app


def init_database():
    default_user = UserService.get_by_username(User, "david19")

    if not default_user:
        default_user = UserService.add_instance(User, 
            username="david19",
            email="david19@gmail.com",
            password= generate_password_hash('testpwd12345', method='sha256'),
            firstname="david", 
            lastname="fernandez", 
            profile_description="data scientist")

    
    columns = {'source':'source', 'target':'target', 'weight':'weight'}
    graph = nw_formatter.file_to_network("./static/game-of-thrones-books/book1.csv", columns)
    network_json = nw_formatter.network_to_json(graph)
    file_hash = hashlib.md5(json.dumps(network_json).encode()).hexdigest()

    dataset = DatasetService.get_by_id(Dataset,
                                       id=file_hash,
                                       user_id=default_user['id'])

    if not dataset:
        DatasetService.add_instance(Dataset,
                                    id=file_hash,
                                    name="book1", 
                                    json=network_json, 
                                    user_id=default_user['id'])


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
