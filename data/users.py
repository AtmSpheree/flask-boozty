import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy_serializer import SerializerMixin
from flask_login import UserMixin


class User(SqlAlchemyBase, SerializerMixin, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String(25), nullable=True)
    surname = sqlalchemy.Column(sqlalchemy.String(25), nullable=True)
    nickname = sqlalchemy.Column(sqlalchemy.String(25), nullable=True)
    avatar = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    about = sqlalchemy.Column(sqlalchemy.String(200), nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String(50),
                              index=True, unique=True, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    posts = orm.relationship('Post', back_populates='user')
    sent_letters = orm.relationship('Letter', secondary='users_to_sent_letters',
                                    backref='who_sent')
    received_letters = orm.relationship('Letter', secondary='users_to_received_letters',
                                        backref='who_received')

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)