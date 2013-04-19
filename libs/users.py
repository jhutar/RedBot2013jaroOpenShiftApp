#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import csv
import path
import base64

import strategies

# Columns of users.csv
# | username | base64str | is_admin |
# TODO: replace base64str with hashed password


class User():
  def __init__(self, username):
    self.username = username
    self.base64str = None
    self.is_admin = None

  def load_details(self):
    user_present = False
    users_csv = csv.reader(open(path.data_path('users.csv'),'r'))
    for row in users_csv:
      if row[0] == self.username:
        self.base64str = row[1]
        self.is_admin = int(row[2])
        user_present = True
        break
    if not user_present:
      raise Exception('User %s do not exists' % username)

  def is_valid(self, base64str):
    """Return true if base64str is `echo -n "user:pass" | openssl enc -base64`
    of some user we have"""
    try:
      self.load_details()
      assert base64str == self.base64str
      return True
    except:
      return False

  def add_user(self, password, is_admin=0):
    # First check user do not exist
    users_csv = csv.reader(open(path.data_path('users.csv'),'r'))
    user_present = False
    for row in users_csv:
      if row[0] == self.username:
        user_present = True
        break
    if user_present:
      raise Exception('User %s already exists' % self.username)
    # Calculate username:password hash
    self.base64str = base64.b64encode('%s:%s' % (self.username, password))
    # Remember is_admin
    self.is_admin = is_admin
    # Add the user
    users_csv = csv.writer(open(path.data_path('users.csv'),'a'))
    users_csv.writerow((self.username, self.base64str, self.is_admin))

  def delete(self, target=None):
    """Delete given user. If user not provided (or set to None) delete
    yourself. Only admin can delete other users."""
    if not target:
      target=self.username
    strats=strategies.get_users_strategies(target)
    for s in strats:
      strategies.delete_stategy(s['label'], target)
    users_csv = csv.reader(open(path.data_path('users.csv'),'r'))
    new=[]
    for u in users_csv:
      if u[0]!=target:
        new.append(u)
    users_csv=csv.writer(open(path.data_path('users.csv'),'w'))
    users_csv.writerows(new)



if __name__ == '__main__':
  # Add admin user
  u_admin = User('redbot_test_admin')
  assert False == u_admin.is_valid(base64.b64encode('redbot_test_admin:test_redbot_admin'))
  u_admin.add_user('test_redbot_admin', 1)
  assert True == u_admin.is_valid(base64.b64encode('redbot_test_admin:test_redbot_admin'))
  assert 1 == u_admin.is_admin
  # Add 2 non-admin users
  u_normal1 = User('redbot_test1')
  u_normal1.add_user('test_redbot', 0)
  assert 0 == u_normal1.is_admin
  u_normal2 = User('redbot_test2')
  u_normal2.add_user('test_redbot', 0)
  assert 0 == u_normal2.is_admin
  # Try to add user with existing name
  added_again = False
  try:
    u_fails = User('redbot_test1')
    u_fails.add_user('', 0)
    added_again = True
  except:
    pass
  assert added_again == False
  # Verify only admin can delete other user
  pass   # TODO: verify only admin can delete other user
