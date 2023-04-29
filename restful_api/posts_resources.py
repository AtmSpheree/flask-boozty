import flask
from flask_restful import reqparse, abort, Resource
from data import db_session
from data.posts import Post
from flask import jsonify
from flask_login import current_user, login_required, UserMixin
from tools.misc import check_is_user_admin_func
from data.tags import Tag
from data.users import User
from sqlalchemy import or_


parser = reqparse.RequestParser()
parser.add_argument('title', required=True)
parser.add_argument('description', required=True)
parser.add_argument('tags', default='')
parser.add_argument('is_opened', type=bool, required=True)
parser.add_argument('invited_users', type=str, default="")


def abort_if_post_not_found(post_id):
    session = db_session.create_session()
    post = session.query(Post).get(post_id)
    if not post:
        abort(404, message=f"Post {post_id} not found")


class PostResource(Resource):
    def get(self, post_id):
        abort_if_post_not_found(post_id)
        session = db_session.create_session()
        post = session.query(Post).get(post_id)
        if current_user is UserMixin:
            if (post.is_opened == 1 or current_user in post.invited_users) or check_is_user_admin_func(current_user.email):
                result = {'post': post.to_dict(
                    only=('title', 'description', 'files', 'is_opened', 'created_date'))}
                result['post']['user_id'] = post.user.id
                result['post']['user_nickname'] = post.user.nickname
                result['post']['tags'] = [i.id for i in post.tags]
                return result
            else:
                abort(404, message=f"You do not have access to Post {post_id}")
        else:
            if post.is_opened == 1:
                result = {'post': post.to_dict(
                    only=('title', 'description', 'files', 'is_opened', 'created_date'))}
                result['post']['user_id'] = post.user.id
                result['post']['user_nickname'] = post.user.nickname
                result['post']['tags'] = [{'id': i.id, 'title': i.title} for i in post.tags]
                return result
            else:
                abort(404, message=f"You do not have access to Post {post_id}")

    @login_required
    def delete(self, post_id):
        abort_if_post_not_found(post_id)
        session = db_session.create_session()
        post = session.query(Post).get(post_id)
        if post.user == current_user or check_is_user_admin_func(current_user.email):
            session.delete(post)
            session.commit()
            return jsonify({'success': 'OK'})
        else:
            abort(404, message=f"You do not have access to delete Post {post_id}")


class PostListResource(Resource):
    def get(self, user_id=None):
        if user_id == "none":
            user_id = None
        session = db_session.create_session()
        if current_user.is_authenticated:
            if user_id is not None:
                if check_is_user_admin_func(current_user.email):
                    posts = session.query(Post).filter(Post.user_id == user_id).all()
                else:
                    posts = session.query(Post).filter(Post.user_id == user_id)
                    posts = [i for i in posts if current_user in i.invited_users or i.is_opened == 1]
            else:
                if check_is_user_admin_func(current_user.email):
                    posts = session.query(Post).all()
                else:
                    posts = session.query(Post).filter(Post.is_opened == 1).all()
        else:
            posts = session.query(Post).filter(Post.is_opened == 1).all()
        result = {'posts': []}
        for item in posts:
            temp = item.to_dict(only=('id', 'title', 'description', 'files', 'is_opened',
                                      'created_date'))
            temp['user_id'] = item.user.id
            temp['user_nickname'] = item.user.nickname
            temp['tags'] = [{'id': i.id, 'title': i.title} for i in item.tags]
            result['posts'] = result['posts'] + [temp]
        return jsonify(result)

    @login_required
    def post(self, user_id=None, args=None):
        if args is None:
            args = parser.parse_args()
            files = ''
        else:
            files = args['files']
        if args['is_opened']:
            invited_users = ''
        else:
            invited_users = args['invited_users']
        tags = args['tags']
        result = {'success': 'OK', 'warning': dict()}
        session = db_session.create_session()
        for item in tags.split(', '):
            if not session.query(Tag).filter(Tag.title == item).first():
                tags = ''
                result['warning']['tags'] = 'tags have not been added'
                break
        if not args['is_opened']:
            for item in invited_users.split(', '):
                if not session.query(User).filter(User.email == item).first() or \
                        session.query(User).filter(User.email == item).first() == current_user:
                    abort(404, message=f"Incorrect input in invited_users")
        if not args['is_opened'] and invited_users == "":
            abort(404, message=f"You must invite at least one user to add a closed post")
        if args['tags'] == "":
            abort(404, message=f"You must add at least one tag to add post")
        post = Post(
            title=args['title'],
            description=args['description'],
            files=files,
            is_opened=args['is_opened'],
            user_id=current_user.id
        )
        for item in tags.split(', '):
            tag = session.query(Tag).filter(Tag.title == item).first()
            post.tags.append(tag)
        if not args['is_opened']:
            for item in invited_users.split(', '):
                user = session.query(User).filter(User.email == item).first()
                post.invited_users.append(user)
        print(2341243)
        session.add(post)
        session.commit()
        return jsonify(result)
