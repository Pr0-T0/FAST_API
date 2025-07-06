import database as _database
import models as _models

def _create_database():
    return _database.Base.metadata.create_all(bind=_database.engine)