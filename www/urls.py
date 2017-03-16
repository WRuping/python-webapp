#!/usr/bin/env python
#_*_ coding: utf-8 _*_
__author__ = 'LYleonard'

import os, re, time, base64, hashlib, logging
from transwarp.web import get, view, post, ctx, interceptor, seeother, notfound
from apis import api, APIError, APIValueError, APIPermissionError, APIResourceNotFoundError
from models import User,Blog, Comment

# @view('test_users.html')
# @get('/')
# def test_users():
#     users = User.find_all()
#     return dict(users=users)

@view('blogs.html')
@get('/')
def index():
    blogs = Blog.find_all()
    user = User.find_first('where email=?', 'admin@example.com')
    return dict(blogs=blogs, user=user)

@api
@get('/api/users')
def api_get_users():
    users = User.find_by('order by created_at desc')
    for u in users:
        u.password = '******'
    return dict(users=users)

