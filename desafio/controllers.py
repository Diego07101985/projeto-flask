import json

from flask import request, jsonify
from typing import Union, Dict
from desafio import app, cache
from desafio.models import User
from desafio.services import ServiceEmail

from desafio.repositorys import RepositoryUsers


RELOAD_COMMAND = ' sudo /usr/sbin/nginx -s reload '
JSON_CONTENT = {'Content-Type': 'application/json'}


@app.route('/reload_nginx', methods=['POST'], strict_slashes=False)
def reload_nginx_in_vm():
    jsonContent = {'Content-Type': 'application/json'}
    if request.method == "POST":
        content = request.get_json()
    else:
        return json.dumps({
            'success': "Error"})

    if content["is_vm_need_reload"]:
        app.logger.info('Ip real %s ', content["real_ip"])

        db.monitor.insert_one({
            # "rpaas-fe-cme": content["rpaas-fe-cme"],
            'vm_status': {
                'real_ip': content["real_ip"],
                'is_vm_need_reload': content["is_vm_need_reload"],
                'access-date': content["access_date"],
                'modify-date': content["modify_date"]
            }
        })

        service_email = ServiceEmail("disalles7@gmail.com",
                                     "disalles222@hotmail.com",
                                     "disalles7@gmail.com", "", "VM teste ", "O IP = "+content["real_ip"])
        service_email.sendEmail()

        return json.dumps({
            # "rpaas-fe-cme": content["rpaas-fe-cme"],
            'vm_status': {
                'real_ip': content["real_ip"],
                'is_vm_need_reload': content["is_vm_need_reload"],
                'access-date': content["access_date"],
                'modify-date': content["modify_date"]
            }
        }), 200, jsonContent
    else:
        return json.dumps({
            "Status": "Essa Vm Nao precisa de Reload"
        }), 200, jsonContent


@app.route("/healthcheck", methods=['GET'], strict_slashes=False)
def healthcheck():
    return jsonify({'status': 'online'})


@app.route('/user/<int:userid>', methods=['DELETE'])
@app.route('/user/<slug>', methods=['DELETE'])
def delete_user(userid=None, slug=None):
    users = RepositoryUsers()
    if userid:
        user = User(id=userid)
    else:
        user = User()
        user.username = slug.title()

    if users.get_user_by_name(user):
        users.delete(user)
        return json.dumps({'message': f'O usuario {user.username} '
                           + 'foi removido com sucesso'}), 200,
        JSON_CONTENT

    return json.dumps({'message': 'Nao existe esse usuario'}), 204,
    JSON_CONTENT


@app.route("/user", methods=['POST'])
def insert_user():
    users = RepositoryUsers()
    # jsonContent = {'Content-Type': 'application/json'}
    content = request.get_json()

    user = User()
    user.username = content['username']
    users = RepositoryUsers()

    if users.get_user_by_name(user):
        return json.dumps({'message': "O usuario ja existe"}), 409,
        JSON_CONTENT

    user.email = content['email']
    user.username = content['username']
    users.insert(user)
    return json.dumps({user.username: {
        "username": user.username,
        "email": user.email}
    }), 200, JSON_CONTENT


@app.route('/user/<int:userid>', methods=["GET"])
@app.route('/user/<slug>', methods=["GET"])
def get_user(userid=None, slug=None):
    users = RepositoryUsers()
    if userid:
        user = User(id=userid)
        user = users.get_user_by_id(user)
    else:
        user = User()
        user.username = slug.title()
        user = users.get_user_by_name(user)

    if not user:
        app.logger.info('User %s', user)
        return json.dumps({}), 204, JSON_CONTENT

    return json.dumps({user.username: {
        "username": user.username,
        "email": user.email

    }
    }), 200, JSON_CONTENT


@app.route('/user', methods=['PUT'])
def update_user():
    users = RepositoryUsers()
    # jsonContent = {'Content-Type': 'application/json'}
    content = request.get_json()

    user = User()
    user.username = content['username']
    if users.get_user_by_name(user):
        if content['email']:
            user.email = content['email']
            user.username = content['username']
            user = users.update(user)
            app.logger.info('%s Update User', user.username)
            return json.dumps({user.username: {
                "username": user.username,
                "email": user.email}
            }), 200, JSON_CONTENT
        else:
            return json.dumps({'message':
                               'Nenhum  email foi enviado para alteracao'}),
            400,
            JSON_CONTENT

    return json.dumps({'message': 'Nao existe esse usuario'}), 204,
    JSON_CONTENT


@app.route("/users", methods=['GET'])
@cache.cached(timeout=50, key_prefix='all_comments')
def get_users():
    users = RepositoryUsers().get_all_user()
    users: Dict[str, Union[str, str]] = {user.username: {
        'nome': user.username, 'email': user.email} for user in users}

    return json.dumps(users), 200, JSON_CONTENT
