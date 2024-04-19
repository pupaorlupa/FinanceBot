from utils.db_api.db_python import BaseModel
# from db_python import BaseModel
import sqlalchemy as sa
from utils.db_api.db_python import db


class Transaction(BaseModel):
    __tablename__ = 'transactions'
    id = sa.Column(sa.Integer, primary_key=True)
    user_id = sa.Column(sa.BigInteger)
    is_income = sa.Column(sa.Boolean)
    category_id = sa.Column(sa.Integer)
    amount = sa.Column(sa.Integer)
    date_created = db.Column(db.DateTime(True), server_default=db.func.now())
    description = db.Column(db.String(250))
    account_id = sa.Column(sa.Integer)
    message_id = sa.Column(sa.BigInteger)

    query: sa.sql.select

