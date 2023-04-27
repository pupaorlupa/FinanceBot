from utils.db_api.db_python import BaseModel
# from db_python import BaseModel
import sqlalchemy as sa


class Account(BaseModel):
    __tablename__ = 'accounts'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(50))
    user_id = sa.Column(sa.BigInteger)
    balance = sa.Column(sa.BigInteger) 
    is_main = sa.Column(sa.Boolean)

    query: sa.sql.select

