from utils.db_api.db_python import BaseModel
# from db_python import BaseModel
import sqlalchemy as sa
from utils.db_api.db_python import db


class CategoryShortcut(BaseModel):
    __tablename__ = 'category_shortcuts'
    id = sa.Column(sa.Integer, primary_key=True)
    user_id = sa.Column(sa.BigInteger)
    name = sa.Column(sa.String(50))
    category_id = sa.Column(sa.BigInteger)

    query: sa.sql.select

