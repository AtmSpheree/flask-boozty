import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


user_to_sent_letter = sqlalchemy.Table(
    'users_to_sent_letters',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('user_id', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('users.id')),
    sqlalchemy.Column('letter_id', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('letters.id'))
)
user_to_received_letter = sqlalchemy.Table(
    'users_to_received_letters',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('user_id', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('users.id')),
    sqlalchemy.Column('letter_id', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('letters.id'))
)


class Letter(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'letters'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String(100), nullable=True)
    description = sqlalchemy.Column(sqlalchemy.String(500), nullable=True)
    files = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
