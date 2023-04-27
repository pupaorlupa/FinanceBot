from utils.db_api.db_python import BaseModel
# from db_python import BaseModel
import sqlalchemy as sa
# from db_python import db
from utils.db_api.db_python import db


class User(BaseModel):
    __tablename__ = 'users'
    user_id = sa.Column(sa.BigInteger, primary_key=True)
    link = sa.Column(sa.String(200))
    date_joined = db.Column(db.DateTime(True),
                            server_default=db.func.now())

    query: sa.sql.select
