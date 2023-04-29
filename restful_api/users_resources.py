from flask_restful import reqparse, abort, Resource
from data import db_session
from data.users import User
from flask import jsonify
from flask_login import login_required, current_user, logout_user
from tools.misc import check_is_user_admin_func
from sqlalchemy import or_


parser = reqparse.RequestParser()
parser.add_argument('name', required=True)
parser.add_argument('surname', required=True)
parser.add_argument('nickname', required=True)
parser.add_argument('about', default='')
parser.add_argument('email', required=True)
parser.add_argument('password', required=True)


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f"User {user_id} not found")


def abort_if_user_exists(email, nickname):
    session = db_session.create_session()
    users = session.query(User).all()
    for user in users:
        if user.email.lower() == email.lower() or user.nickname.lower() == nickname.lower():
            abort(404, message=f"A user with such an email and/or nickname already exists")


class UserResource(Resource):
    @login_required
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        if current_user == user:
            return jsonify({'user': user.to_dict(
                only=('name', 'surname', 'nickname', 'avatar', 'about',
                      'email', 'created_date'))})
        else:
            return jsonify({'user': user.to_dict(
                only=('nickname', 'avatar', 'about',
                      'email', 'created_date'))})

    @login_required
    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        if user == current_user or check_is_user_admin_func(current_user.email):
            session.delete(user)
            session.commit()
            if user == current_user:
                logout_user()
            return jsonify({'success': 'OK'})
        else:
            abort(404, message=f'You do not have access to delete User {user_id}')


class UserListResource(Resource):
    @login_required
    def get(self, args=None):
        session = db_session.create_session()
        users = session.query(User).all()
        if check_is_user_admin_func(current_user.email):
            response = jsonify({'users': [item.to_dict(
                               only=('name', 'surname', 'nickname', 'avatar', 'about', 'email',
                                     'created_date')) for item in users]})
        else:
            response = jsonify({'users': [item.to_dict(
                only=('nickname', 'avatar', 'about', 'email',
                      'created_date')) for item in users]})
        # response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    def post(self, args=None):
        if args is None:
            args = parser.parse_args()
            avatar = ''
        else:
            avatar = args['avatar']
        abort_if_user_exists(args['email'], args['nickname'])
        session = db_session.create_session()
        user = User(
            name=args['name'],
            surname=args['surname'],
            nickname=args['nickname'],
            about=args['about'],
            email=args['email'],
            avatar=avatar
        )
        user.set_password(args['password'])
        session.add(user)
        session.commit()
        return jsonify({'success': 'OK'})
