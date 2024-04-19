from utils.db_api.db_python import BaseModel
# from db_python import BaseModel
import sqlalchemy as sa
from utils.db_api.db_python import db


class AccountShortcut(BaseModel):
    __tablename__ = 'account_shortcuts'
    id = sa.Column(sa.Integer, primary_key=True)
    user_id = sa.Column(sa.BigInteger)
    name = sa.Column(sa.String(50))
    account_id = sa.Column(sa.Integer)

    query: sa.sql.select

