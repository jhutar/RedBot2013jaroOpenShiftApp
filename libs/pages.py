#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import html
import strategies
import path
import games
import users

from tempfile import TemporaryFile
import os, cgi

def is_authorized(environ):
  if 'HTTP_AUTHORIZATION' not in environ:
    return False
  auth = environ['HTTP_AUTHORIZATION'].split(' ')[1]
  username, password = auth.decode('base64').split(':', 1)
  u = users.User(username)
  return u.is_valid(auth)

def main(environ):
  response_body = html.header('Ahoy!', False)
  response_body += html.welcome()
  response_body += html.footer()
  return response_body

def menu(environ):
  response_body = html.header('Ahoy!')
  response_body += html.menu()
  response_body += html.footer()
  return response_body

def game(environ):
  response_body = html.header('Ahoy!')
  response_body += html.form_create_new_game(strategies.get_strategies())
  response_body += html.footer()
  return response_body

def game_new(environ):
  post = path.get_post_array(environ)
  g = games.Game(None, post['strat1'][0], post['strat2'][0], 'aaa@bbbbb.cc')
  return g

def user(environ):
  response_body = html.header('Ahoy!', False)
  response_body += html.form_create_new_user()
  response_body += html.footer()
  return response_body

def user_new(environ):
  post = path.get_post_array(environ)
  if post['test'][0]!="8":
    raise Exception('Begone!')
  u=users.User(post['username'][0])
  u.add_user(post['password'][0])
  return html.header('Ahoy!', False)+html.user_new(post['username'][0])+html.footer()

def strategy(environ):
  response_body = html.header('Ahoy!')
  response_body += html.form_new_strategy()
  response_body += html.footer()
  return response_body

def read(environ):
  length = int(environ.get('CONTENT_LENGTH', 0))
  stream = environ['wsgi.input']
  body = TemporaryFile(mode='w+b')
  while length > 0:
    part = stream.read(min(length, 1024*200)) # 200KB buffer size
    if not part: break
    body.write(part)
    length -= len(part)
  body.seek(0)
  environ['wsgi.input'] = body
  return body

def strategy_new(environ):
  body=read(environ)
  form=cgi.FieldStorage(fp=body, environ=environ, keep_blank_values=True)
  auth = environ['HTTP_AUTHORIZATION'].split(' ')[1]
  username, password = auth.decode('base64').split(':', 1)
  strategies.add_strategy(form.getvalue("name") ,form.getvalue("file"), username)
  return html.header('Ahoy!')+html.strat_new()+html.footer()

def strats(environ):
  auth = environ['HTTP_AUTHORIZATION'].split(' ')[1]
  username, password = auth.decode('base64').split(':', 1)
  strats=strategies.get_users_strategies(username)
  response_body=html.header('Ahoy!')
  response_body+=html.strats(strats)
  response_body+=html.footer()
  return response_body

def strats_delete(environ):
  auth = environ['HTTP_AUTHORIZATION'].split(' ')[1]
  username, password = auth.decode('base64').split(':', 1)
  label=environ['PATH_INFO'].split('/')[-1]
  strategies.delete_stategy(label, username)
  response_body=html.header('Ahoy!')
  response_body+=html.strat_delete(label)
  response_body+=html.footer()
  return response_body

def delete(environ):
  response_body=html.header('Ahoy!')
  response_body+=html.delete()
  response_body+=html.footer()
  return response_body

def delete_yes(environ):
  auth = environ['HTTP_AUTHORIZATION'].split(' ')[1]
  username, password = auth.decode('base64').split(':', 1)
  u=users.User(username)
  u.delete()
  return main(environ)

def game_show(environ):
  response_body = html.header('Ahoy!')
  uri = environ['PATH_INFO'].split('/')
  g = games.Game(uri[3])
  response_body += html.show_game(g)
  g.play()
  response_body += '<pre>%s</pre>' % g.stdoutdata
  response_body += html.show_game(g)
  response_body += html.footer()
  return response_body
