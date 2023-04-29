from flask import Flask, redirect, render_template, abort, request, jsonify
import json
import os
from data import db_session
from flask_restful import Api
from forms.loginform import LoginForm
import forms.registerform as registerform
import forms.addpostform as addpostform
import forms.addtagform as addtagform
from flask_uploads import UploadSet, configure_uploads, patch_request_class, secure_filename
from restful_api import users_resources, posts_resources, letters_resources, tags_resources
from flask_login import LoginManager, logout_user, login_required, login_user, current_user, UserMixin
from data.users import User
from data.posts import Post
from data.tags import Tag
from variables import (UPLOAD_FOLDER, MAX_CONTENT_LENGTH_BYTES, MAX_FILES_COUNT)
import variables
from tools.misc import translit_ru_to_en, test_is_photo, get_only_photos_files, get_tags_title, check_is_user_admin, check_is_user_admin_func


with open('connetion.json', 'r') as data:
    dictionary = json.load(data)
    host, port, db_path = dictionary['host'], dictionary['port'], dictionary['db']
app = Flask(__name__)
api = Api(app)
db_session.global_init(db_path)
login_manager = LoginManager()
login_manager.init_app(app)
api.add_resource(users_resources.UserListResource, '/api/user')
api.add_resource(users_resources.UserResource, '/api/user/<int:user_id>')
api.add_resource(posts_resources.PostListResource, '/api/posts/<user_id>')
api.add_resource(posts_resources.PostResource, '/api/post/<int:post_id>')
api.add_resource(letters_resources.LetterListResource, '/api/letter/<int:user_id>')
api.add_resource(letters_resources.LetterResource, '/api/letter/<int:letter_id>')
api.add_resource(tags_resources.TagListResource, '/api/tag')
api.add_resource(tags_resources.TagResource, '/api/tag/<int:tag_id>')
app.config['SECRET_KEY'] = 'boozty_service_secret_key'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['UPLOADS_DEFAULT_DEST'] = os.path.join(basedir, UPLOAD_FOLDER)
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH_BYTES
configure_uploads(app, variables.photos)
configure_uploads(app, variables.files)
patch_request_class(app, None)


def get_avatar_path():
    if not isinstance(current_user, UserMixin):
        avatar_path = ''
    else:
        avatar_path = variables.photos.url(current_user.avatar)
    return avatar_path


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).filter(User.id == user_id).first()


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               title='Авторизация',
                               message="Неправильный логин или пароль.",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form,
                           avatar_path=get_avatar_path())


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = registerform.RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        req = {'name': form.name.data,
               'surname': form.surname.data,
               'nickname': form.nickname.data,
               'about': form.about.data,
               'email': form.email.data,
               'password': form.password.data,
               'avatar': ''}
        if form.avatar.data:
            filename = translit_ru_to_en(form.avatar.data.filename)
            filename = variables.photos.save(form.avatar.data, name=secure_filename(filename))
            req['avatar'] = filename
        res = users_resources.UserListResource().post(req)
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form,
                           avatar_path=get_avatar_path())


@app.route('/add_post', methods=['GET', 'POST'])
@login_required
def add_post():
    form = addpostform.AddPostForm()
    if form.validate_on_submit():
        req = {'title': form.title.data,
               'description': form.description.data,
               'is_opened': form.is_opened.data,
               'tags': form.tags.data,
               'invited_users': form.invited_users.data}
        files = []
        for item in form.files.data:
            if not item.filename:
                continue
            filename = translit_ru_to_en(item.filename)
            filename = variables.files.save(item, name=secure_filename(filename))
            files.append(filename)
        if len(files) > variables.MAX_FILES_COUNT:
            abort(404)
        req['files'] = ', '.join(files)
        res = posts_resources.PostListResource().post(args=req)
        if res.json['success'] == 'OK':
            return redirect('/')
        else:
            abort(404)
    tags = tags_resources.TagListResource().get().json['tags']
    return render_template('add_post.html', title='Добавление записи', form=form,
                           avatar_path=get_avatar_path(),
                           json_file_variables=json.dumps(variables.data),
                           tags=tags)


@app.errorhandler(413)
def file_is_too_large_error(error):
    return render_template('413.html', avatar_path=get_avatar_path()), 413


@app.errorhandler(401)
def unauthorized(error):
    return render_template('413.html', avatar_path=get_avatar_path()), 401


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', avatar_path=get_avatar_path()), 404


@app.route('/')
def index():
    accessed_tags = []
    accessed_tags = request.args.get('tags')
    posts = posts_resources.PostListResource().get().json['posts']
    if accessed_tags and accessed_tags != '':
        try:
            accessed_tags = list(map(int, accessed_tags.split(';')))
        except Exception:
            abort(404)
        session = db_session.create_session()
        for i in accessed_tags:
            tag = session.query(Tag).filter(Tag.id == i)
            if not tag:
                abort(404)
        posts = [i for i in posts if set([k["id"] for k in i["tags"]]).issuperset(set(accessed_tags))]
    tags = tags_resources.TagListResource().get().json['tags']
    tags.insert(0, {'title': 'Все'})
    if not isinstance(current_user, UserMixin):
        avatar_path = ''
    else:
        avatar_path = variables.photos.url(current_user.avatar)
    return render_template('index.html', title='Boozty', posts=posts,
                           tags=tags, avatar_path=avatar_path,
                           url_func=variables.files.url,
                           test_is_photo=test_is_photo,
                           get_only_photos_files=get_only_photos_files,
                           accessed_tags=json.dumps(accessed_tags),
                           get_tags_title=get_tags_title,
                           check_is_user_admin_func=check_is_user_admin_func)


@app.route('/user/<int:user_id>')
def user_page(user_id: int):
    user = users_resources.UserResource().get(user_id).json['user']
    posts = posts_resources.PostListResource().get(user_id).json
    if user["avatar"]:
        avatar_path = variables.photos.url(user["avatar"])
    else:
        avatar_path = "/static/img/standart_avatar.png"
    return render_template('user_page.html', title=user["nickname"],
                           posts=posts["posts"], user=user,
                           avatar_path=avatar_path,
                           test_is_photo=test_is_photo,
                           get_only_photos_files=get_only_photos_files,
                           url_func=variables.files.url,
                           get_tags_title=get_tags_title)


@app.route('/add_tag', methods=['GET', 'POST'])
@login_required
@check_is_user_admin
def add_tag():
    form = addtagform.AddTagForm()
    if form.validate_on_submit():
        req = {'title': form.title.data}
        session = db_session.create_session()
        tags = [i.title for i in session.query(Tag).all()]
        if form.title.data in tags:
            return render_template('add_tag.html', title='Добавление тэга', form=form,
                                   message='Такой тэг уже существует!',
                                   avatar_path=get_avatar_path())
        res = tags_resources.TagListResource().post(args=req)
        if res.json['success'] == 'OK':
            return redirect('/')
        else:
            abort(404)
    return render_template('add_tag.html', title='Добавление тэга', form=form,
                           avatar_path=get_avatar_path())


@app.route('/letters')
@login_required
def letters():
    sent_letters = current_user.sent_letters
    received_letters = current_user.received_letters
    return render_template('letters.html', title='Письма',
                           avatar_path=get_avatar_path())


if __name__ == '__main__':
    # session = db_session.create_session()
    # tag = Tag()
    # tag.title = 'Кино'
    # session.add(tag)
    # tag = Tag()
    # tag.title = 'Музыка'
    # session.add(tag)
    # session.commit()
    # session = db_session.create_session()
    # for i in session.query(Post).all():
    #     session.delete(i)
    # session.commit()
    app.run(port=port, host=host)
