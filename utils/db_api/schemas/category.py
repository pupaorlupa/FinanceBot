from utils.db_api.db_python import BaseModel
# from db_python import BaseModel
import sqlalchemy as sa
from utils.db_api.db_python import db
# from db_python import db


class Category(BaseModel):
    __tablename__ = 'categories'
    id = db.Column(db.BigInteger, primary_key=True)
    name = sa.Column(sa.String(50))
    user_id = sa.Column(sa.BigInteger)
    is_income = sa.Column(sa.Boolean)

    query: sa.sql.select
