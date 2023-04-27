import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


post_to_user = sqlalchemy.Table(
    'posts_to_users',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('post_id', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('posts.id')),
    sqlalchemy.Column('user_id', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('users.id'))
)


class Post(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'posts'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String(50), nullable=True)
    description = sqlalchemy.Column(sqlalchemy.String(1000), nullable=True)
    files = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    is_opened = sqlalchemy.Column(sqlalchemy.Boolean(), default=False)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'),
                                nullable=True)
    invited_users = orm.relationship('User', secondary='posts_to_users',
                                     backref='available_posts')
    user = orm.relationship('User')
    tags = orm.relationship('Tag', secondary='tags_to_posts',
                            backref='posts')
