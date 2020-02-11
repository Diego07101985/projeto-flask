import os
from flask import request, jsonify
import json
from sre import app
import subprocess
import hashlib
from base64 import b64decode
import logging

RELOAD_COMMAND = ' sudo /usr/sbin/nginx -s reload '


@app.route('/reload_nginx', methods=['POST'], strict_slashes=False)
def reload_nginx_in_vm():
    jsonContent = {'ContentType': 'application/json'}
    status = 0
    if request.method == "POST":
        content = request.get_json()
    else:
        return json.dumps({
            'success': "Error"})

    if content["is_vm_need_reload"] == True:
        app.logger.info('Ip real %s ', content["real_ip"])
        return json.dumps({
            # "rpaas-fe-cme": content["rpaas-fe-cme"],
            'vm_status': {
                'real_ip': content["real_ip"],
                'is_vm_need_reload': content["is_vm_need_reload"],
                "access-date": content["access_date"],
                "modify-date": content["modify_date"]
            }
        }), 200, jsonContent
    else:
        return json.dumps({
            "Status": "Essa Vm Nao precisa de Reload"
        }), 200, jsonContent


@app.route("/healthcheck", methods=['GET'], strict_slashes=False)
def healthcheck():
    return jsonify({'status': 'online'})
