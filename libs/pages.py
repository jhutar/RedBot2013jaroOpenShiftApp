#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import html
import strategies
import path
import games
import users

def is_authorized(environ):
  if 'HTTP_AUTHORIZATION' not in environ:
    return False
  auth = environ['HTTP_AUTHORIZATION'].split(' ')[1]
  username, password = auth.decode('base64').split(':', 1)
  u = users.User(username)
  return u.is_valid(auth)

def main(environ):
  response_body = html.header('Ahoy!')
  response_body += html.welcome()
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
