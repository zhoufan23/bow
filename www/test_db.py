#!/usr/bin/env python
# coding=utf-8

__author__ = 'Felix Zhou'

from models import User

from transwarp import db

db.create_engine(user='bow', password='bow', database='bow')
db.update('drop table if exists user')
db.update(User().__sql__)

u = User(name='Test', email='test@example.com', password='1234567890', image='about:blank')

u.insert()

print 'new user id:', u.id

u1 = User.find_first('where email=?', 'test@example.com')
print 'find user\'s name:', u1.name

u1.delete()

u2 = User.find_first('where email=?', 'test@example.com')
print 'find user:', u2
