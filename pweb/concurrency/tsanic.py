#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Created on    : 18/1/10 下午4:45
# @Author  : zpy
# @Software: PyCharm

from sanic import Sanic, request, response
from sanic.response import text

app = Sanic(__name__)



@app.route('/')
async def index(request):
    return text("hello world")

@app.route('/post', methods=['GET', 'POST'])
async def test_post(request):
    data = request.json
    return text(str(data))

@app.route('/redirect')
async def test_redirect(request):
    return response.redirect(app.url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
