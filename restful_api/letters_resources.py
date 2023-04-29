from flask_restful import reqparse, abort, Resource
from data import db_session
from data.letters import Letter
from data.users import User
from flask import jsonify
from flask_login import login_required, current_user
from tools.misc import check_is_user_admin_func

parser = reqparse.RequestParser()
parser.add_argument('title', required=True)
parser.add_argument('description', default='')
parser.add_argument('files', default='')
parser.add_argument('receiver', required=True)


def abort_if_letter_not_found(letter_id):
    session = db_session.create_session()
    letter = session.query(Letter).get(letter_id)
    if not letter:
        abort(404, message=f"Letter {letter_id} not found")


class LetterResource(Resource):
    @login_required
    def get(self, letter_id):
        abort_if_letter_not_found(letter_id)
        session = db_session.create_session()
        letter = session.query(Letter).get(letter_id)
        if letter in current_user.sent_letters or \
                letter in current_user.received_letters or \
                check_is_user_admin_func(current_user.email):
            return jsonify({'letter': letter.to_dict(
                only=('title', 'description', 'files', 'created_date'))})
        else:
            abort(404, message=f"You do not have access to Letter {letter_id}")

    @login_required
    def delete(self, letter_id):
        abort_if_letter_not_found(letter_id)
        session = db_session.create_session()
        letter = session.query(Letter).get(letter_id)
        if letter in current_user.sent_letters:
            session.delete(letter)
            session.commit()
            return jsonify({'success': 'OK'})
        elif letter in current_user.received_letters:
            current_user.received_letters.remove(letter)
            session.commit()
            return jsonify({'success': 'OK'})
        elif check_is_user_admin_func(current_user.email):
            session.delete(letter)
            session.commit()
            return jsonify({'success': 'OK'})
        else:
            abort(404, message=f"You do not have access to delete Letter {letter_id}")


class LetterListResource(Resource):
    @login_required
    def get(self, user_id=None):
        session = db_session.create_session()
        letters = []
        if user_id is not None:
            if check_is_user_admin_func(current_user.email):
                user = session.query(User).filter(User.id == user_id).first()
                sent_letters = user.sent_letters
                received_letters = user.received_letters
            else:
                if user_id == current_user.id:
                    sent_letters = current_user.sent_letters
                    received_letters = current_user.received_letters
                else:
                    user = session.query(User).filter(User.id == user_id).first()
                    sent_letters = session.query(Letter).filter(user in Letter.who_received,
                                                                current_user in Letter.who_sent).all()
                    received_letters = session.query(Letter).filter(user in Letter.who_sent,
                                                                    current_user in Letter.who_received).all()
        else:
            if check_is_user_admin_func(current_user.email):
                letters = session.query(Letter).all()
            else:
                sent_letters = current_user.sent_letters
                received_letters = current_user.received_letters
        if letters:
            result = {'letters': [item.to_dict(
                only=('id', 'title', 'description', 'created_date',
                      'who_sent', 'who_received')) for item in letters]}
            for i in range(len(result['letters'])):
                result['letters'][i]['who_sent'] = result['letters'][i]['who_sent'].id
                result['letters'][i]['who_received'] = result['letters'][i]['who_received'].id
            return jsonify(result)
        else:
            result = {'sent_letters': [item.to_dict(
                only=('id', 'title', 'description', 'created_date',
                      'who_sent', 'who_received')) for item in sent_letters],
                      'received_letters': [item.to_dict(
                only=('id', 'title', 'description', 'created_date',
                      'who_sent', 'who_received')) for item in received_letters]}
            for i in range(len(result['sent_letters'])):
                result['sent_letters'][i]['who_sent'] = {'id': result['sent_letters'][i]['who_sent'].id,
                                                         'nickname': result['sent_letters'][i]['who_sent'].nickname}
                result['sent_letters'][i]['who_received'] = {'id': result['sent_letters'][i]['who_received'].id,
                                                             'nickname': result['sent_letters'][i]['who_received'].nickname}
            for i in range(len(result['received_letters'])):
                result['received_letters'][i]['who_sent'] = {'id': result['received_letters'][i]['who_sent'].id,
                                                             'nickname': result['received_letters'][i]['who_sent'].nickname}
                result['received_letters'][i]['who_received'] = {'id': result['received_letters'][i]['who_received'].id,
                                                                 'nickname': result['received_letters'][i]['who_received'].nickname}
            return jsonify(result)

    @login_required
    def post(self, user_id=None):
        result = {'success': 'OK', 'warning': dict()}
        args = parser.parse_args()
        session = db_session.create_session()
        files = args['files']
        for item in files.split(', '):
            try:
                open(item)
            except Exception:
                files = ''
                result['warning']['files'] = 'files have not been added'
                break
        letter = Letter(
            title=args['name'],
            description=args['description'],
            files=files
        )
        session.add(letter)
        session.commit()
        return jsonify(result)
