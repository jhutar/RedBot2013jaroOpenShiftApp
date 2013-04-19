#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# TODO: we should be HTML escaping whenever we print something

def header(title='Ahoy!', show_menu=True):
  ret = ''
  ret += '''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
'''
  ret += "<title>%s</title>" % title
  ret += '''
  <style>
  html { 
  background: black;
  }
  body {
    background: #333;
    background: -webkit-linear-gradient(top, #222, #666);
    background: -o-linear-gradient(top, #222, #666);
    background: -moz-linear-gradient(top, #222, #666);
    background: linear-gradient(top, #222, #666);
    color: white;
    font-family: "Helvetica Neue",Helvetica,"Liberation Sans",Arial,sans-serif;
    width: 40em;
    margin: 0 auto;
    padding: 3em;
   
  }
  a {
    color: white;
  }

  h1 {
    text-transform: capitalize;
    -moz-text-shadow: -1px -1px 0 black;
    -webkit-text-shadow: 2px 2px 2px black;
    text-shadow: -1px -1px 0 black;
    box-shadow: 1px 2px 2px rgba(0, 0, 0, 0.5);
    background: #C00;
    width: 22.5em;
    margin: 1em -2em;
    padding: .3em 0 .3em 1.5em;
    position: relative;
  }
  h2 { 
    margin: 2em 0 .5em;
    border-bottom: 1px solid #999;
  }
  pre {
    background: black;
    padding: 1em 0 0;
    -webkit-border-radius: 1em;
    -moz-border-radius: 1em;
    border-radius: 1em;
    color: #9cf;
  }
  </style>
</head>
<body>'''
  ret += "  <h1>%s</h1>" % title
  if(show_menu):
    ret+='''<div style="float: left; width: 20;"><ul>
  <li><a href="/game">Play a game</a></li>
  <li><a href="/strat">Upload a strategy</a></li>
  <li><a href="/strats">Show my strategies</a></li>
  <li><a href="/delete">Delete this profile</a></li>
  </ul></div>
  <div style="float: right;">'''
  return ret

def welcome():
  return '''<p><a href="/menu">Log-in<a> or <a href="/user">Sign-up</a>.</p>'''

def menu():
    return '''Welcome.'''

def form_create_new_game(mystrategies):
  ret = '<h2>Create new game</h2>'
  ret += '<form method="POST" action="/game/new">'
  ret += '<select name="strat1">'
  for s in mystrategies:
    ret += '<option value="%s">%s</option>' % (s['label'], s['name'])
  ret += '</select>'
  ret += '<select name="strat2">'
  for s in mystrategies:
    ret += '<option value="%s">%s</option>' % (s['label'], s['name'])
  ret += '</select>'
  ret += '<input type="submit"/>'
  ret += '</form>'
  return ret

def show_game(mygame):
  ret = '<h2>Game %s</h2>' % mygame.gameid
  ret += '<p>Owner: %s</p>' % mygame.owner
  ret += '<p>Directory: %s</p>' % mygame.gamedir
  ret += '<p>Strategy 1: %s</p>' % mygame.strat1
  ret += '<p>Strategy 2: %s</p>' % mygame.strat2
  ret += '<p>Rounds played: %s</p>' % mygame.round
  return ret

def form_create_new_user():
  ret = '<h2>Create new user</h2>'
  ret += '<form method="POST" action="/user/new">'
  ret += 'Username: <input type="text" name="username"><br>'
  ret += 'Password: <input type="password" name="password"><br>'
  ret += '2+7*2-8: <input type="text" name="test"><br>'
  ret += '<input type="submit" value="Create!"/>'
  ret += '</form>'
  return ret

def form_new_strategy():
  ret = '<h2>Upload new strategy</h2>'
  ret += '<form enctype="multipart/form-data"  method="POST" action="/strat/new">'
  ret += 'Name: <input type="text" name="name" id="name"><br>'
  ret += 'File: <input type="file" name="file" id="file"><br>'
  ret += '<input type="submit" value="Upload!"/>'
  ret += '</form>'
  return ret

def user_new(username):
  return 'User "%s" was created.'%username

def strat_new():
  return 'Strategy was uploaded.'

def strats(strats):
  r='<ul>'
  for s in strats:
    r+='<li>{0} <a href="/strats/delete/{1}">delete</a></li>'.format(s['name'], s['label'])
  r+='</ul>'
  return r

def strat_delete(label):
  return 'Strategy \"{0}\" was deleted.'.format(label)

def delete():
  return 'Do you really want to delete yourself?<br><a href="/delete/yes">Yes</a> or <a href="/menu">No</a>.'

def footer():
  return '''</div>
</body>
</html>'''
