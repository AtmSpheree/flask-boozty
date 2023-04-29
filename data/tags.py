import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


tag_to_post = sqlalchemy.Table(
    'tags_to_posts',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('tag_id', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('tags.id')),
    sqlalchemy.Column('post_id', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('posts.id'))
)


class Tag(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'tags'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String(25), nullable=True)
