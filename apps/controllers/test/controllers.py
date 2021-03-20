# -*- coding: utf-8 -*-
import requests
from flask import Blueprint, abort, render_template, request

from apps.common.response import ok, error
from apps.database.models import Test
from .forms import TestForm

app = Blueprint('test', __name__, url_prefix='/test')


@app.route('/ping', methods=['GET'])
def ping():
    return ok('pong')


@app.route('/proxy', methods=['GET', 'POST'])
def proxy():
    args = request.args
    form = request.form
    url = args.get('url')

    if not url:
        return error(50000)

    if request.method == 'GET':
        res = requests.get(url=url)
    else:
        res = requests.post(url=url, data=form)

    return ok(dict(url=res.url, data=res.text, code=res.status_code))


@app.route('/db', methods=['GET'])
def db():
    test = Test.query.first()
    if test:
        message = test.message
    else:
        message = None
    return ok({'message': message})


@app.route('/403', methods=['GET'])
def forbidden():
    return abort(403)


@app.route('/404', methods=['GET'])
def page_not_found():
    return abort(404)


@app.route('/410', methods=['GET'])
def gone():
    return abort(410)


@app.route('/500', methods=['GET'])
def internal_server_error():
    return abort(500)


@app.route('/html', methods=['GET', 'POST'])
def html():
    form = TestForm()

    fruits = {'apple': '사과', 'orange': '오렌지', 'grape': '포도'}
    for key in fruits.keys():
        form.fruits.choices.append((key, fruits[key]))

    if form.validate_on_submit():
        return render_template('test/html.html', form=form, result='저장했습니다.')

    return render_template('test/html.html', form=form)
