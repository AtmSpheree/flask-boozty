import json
from flask import abort
from flask_login import current_user

import variables

TRANSLIT = {'а': 'a', 'б': 'b', 'в': 'v',
            'г': 'g', 'д': 'd', 'е': 'e',
            'ё': 'e', 'ж': 'j', 'з': 'z',
            'и': 'i', 'й': 'y', 'к': 'k',
            'л': 'l', 'м': 'm', 'н': 'n',
            'о': 'o', 'п': 'p', 'р': 'r',
            'с': 's', 'т': 't', 'у': 'u',
            'ф': 'f', 'х': 'h', 'ц': 'c',
            'ч': 'ch', 'ш': 'sh', 'щ': 'sh',
            'ъ': '', 'ы': 'i', 'ь': '',
            'э': 'e', 'ю': 'u', 'yu': 'ya'}


def translit_ru_to_en(text):
    result = ''
    for item in text:
        if item in TRANSLIT:
            result += TRANSLIT[item]
        else:
            result += item
    if not result or result[0] == '.':
        result = 'deleted_russian_name' + result
    return result


def check_is_user_admin_func(email):
    with open('root.json', 'r') as data:
        dictionary = json.load(data)
        admin_users = dictionary['users']['admin']
    if any(map(lambda x: x['email'] == email, admin_users)):
        return True
    return False


def check_is_user_admin(func):
    def decorated_func(*args, **kwargs):
        email = current_user.email
        if check_is_user_admin_func(email):
            return func(*args, **kwargs)
        else:
            abort(404, message="You do not have access to delete users")
    return decorated_func


def test_is_photo(string):
    if string:
        base = string.split('.')[1]
    else:
        return False
    if base.lower() in [i.lower() for i in variables.ALLOWED_EXTENSIONS_PHOTOS]:
        return True
    return False


def get_only_photos_files(array):
    return [i for i in array if test_is_photo(i)]


def get_tags_title(tags):
    return [i["title"] for i in tags]
