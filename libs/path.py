#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os.path
import urlparse

def data_path(*args):
  return os.path.join(os.environ['OPENSHIFT_REPO_DIR'], 'data', *args)

def get_post_array(environ):
  try:
    request_body_size = int(environ.get('CONTENT_LENGTH', 0))
  except (ValueError):
    request_body_size = 0
  request_body = environ['wsgi.input'].read(request_body_size)
  post = urlparse.parse_qs(request_body)
  return post
