from flask_restful import reqparse, abort, Resource
from data import db_session
from data.tags import Tag
from flask import jsonify
from flask_login import login_required
from tools.misc import check_is_user_admin


parser = reqparse.RequestParser()
parser.add_argument('title', required=True)


def abort_if_tag_not_found(tag_id):
    session = db_session.create_session()
    tag = session.query(Tag).get(tag_id)
    if not tag:
        abort(404, message=f"Tag {tag_id} not found")


class TagResource(Resource):
    @login_required
    def get(self, tag_id):
        abort_if_tag_not_found(tag_id)
        session = db_session.create_session()
        tag = session.query(Tag).get(tag_id)
        return jsonify({'tag': tag.to_dict(
            only=('title'))})

    @login_required
    @check_is_user_admin
    def delete(self, tag_id):
        abort_if_tag_not_found(tag_id)
        session = db_session.create_session()
        tag = session.query(Tag).get(tag_id)
        session.delete(tag)
        session.commit()
        return jsonify({'success': 'OK'})


class TagListResource(Resource):
    def get(self):
        session = db_session.create_session()
        tags = session.query(Tag).all()
        return jsonify({'tags': [item.to_dict(
            only=('id', 'title')) for item in tags]})

    @login_required
    @check_is_user_admin
    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        title = args['title']
        for tag in session.query(Tag).all():
            if tag.title == title:
                abort(404, message='Tag with this title is already exists')
        tag = Tag(
            title=title
        )
        session.add(tag)
        session.commit()
        return jsonify({'success': 'OK'})
