#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Created on    : 18/1/10 下午4:45
# @Author  : zpy
# @Software: PyCharm

from flask import Flask, request, redirect, url_for
from flask_common import Common

app = Flask(__name__)
common = Common(app)

@app.route('/')
def index():
    return "hello world"

@app.route('/post', methods=['GET', 'POST'])
def test_post():
    data = request.json
    return str(data)

@app.route('/redirect')
def test_redirect():
    return redirect(url_for('.index'))


if __name__ == '__main__':
    # app.run(debug=True)
    common.serve()

