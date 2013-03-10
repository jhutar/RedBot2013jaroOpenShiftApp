#!/usr/bin/env python
# -*- coding: UTF-8 -*-

def header(title='Ahoy!'):
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
  return ret

def footer():
  return '''</body>
</html>'''
