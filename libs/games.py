#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import tempfile
import strategies
import shutil
import ConfigParser
import time
import path
import subprocess
import csv

class Game():

  strat1id = 'strat1'
  strat2id = 'strat2'

  def __init__(self, gameid=None, strat1=None, strat2=None, owner=None):
    self.stdoutdata = None
    self.stderrdata = None
    if gameid == None:
      # TODO: There should be some limit for games opened in parallel
      assert strat1 != None
      assert strat2 != None
      assert owner != None
      self.round = 0
      self.owner = owner
      # Deploy files into game dir
      self.gamedir = tempfile.mkdtemp()
      self.gameid = os.path.basename(self.gamedir)
      shutil.copy(path.data_path('redbot'), self.gamedir)
      self.strat1 = strategies.Strategy(strat1)
      self.strat1.deploy(self.gamedir, self.strat1id)
      self.strat2 = strategies.Strategy(strat2)
      self.strat2.deploy(self.gamedir, self.strat2id)
      os.mkdir(os.path.join(self.gamedir, 'replay'))
      # Create INI file with details
      self.dump_ini()
      # Add a line into global CSV file
      games_csv = csv.writer(open(path.data_path('games.csv'),'a'))
      games_csv.writerow((self.gameid, self.owner))
    else:
      assert strat1 == None
      assert strat2 == None
      assert owner == None
      # Game already exists
      self.gameid = gameid
      # Load details from INI file
      self.load_ini()

  def dump_ini(self):
    ini = ConfigParser.SafeConfigParser()
    ini.add_section('Game')
    ini.set('Game', 'owner', self.owner)
    ini.set('Game', 'created', str(int(time.time())))
    ini.set('Game', self.strat1id, self.strat1.label)
    ini.set('Game', self.strat2id, self.strat2.label)
    ini.set('Game', 'round', str(self.round))
    ini.write(open(os.path.join('/tmp', self.gameid, 'info.ini'), 'w'))   # TODO: make this work when not on /tmp

  def load_ini(self):
    ini = ConfigParser.SafeConfigParser()
    self.gamedir = os.path.join('/tmp', self.gameid)   # TODO: make this work when not on /tmp
    ini.readfp(open(os.path.join(self.gamedir, 'info.ini'), 'r'))
    self.strat1 = strategies.Strategy(ini.get('Game', self.strat1id))
    self.strat2 = strategies.Strategy(ini.get('Game', self.strat2id))
    self.owner = ini.get('Game', 'owner')
    self.round = int(ini.get('Game', 'round'))

  ###def play(self, round):
  def play(self):
    ###assert round == self.round+1
    ###assert isinstance(round, int)
    if not ( self.strat1.is_ready(self.gamedir, self.strat1id, round) \
        and self.strat2.is_ready(self.gamedir, self.strat2id, round) ):
      return False
    d=os.getcwd()
    os.chdir(self.gamedir)
    #print "DEBUG: Playing %s. round" % round
    p = subprocess.Popen(['./redbot', '-b', 'replay', os.path.join(self.strat1id, self.strat1.label), os.path.join(self.strat2id, self.strat2.label)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)   # TODO: there should be some limit for parallel redbot processes count
    (self.stdoutdata, self.stderrdata) = p.communicate()
    assert self.stderrdata == ''
    ###self.round += 1
    self.round = 150
    self.dump_ini()
    os.chdir(d)

  def cleanup(self):
    shutil.rmtree(self.gamedir)
    # TODO: also delete line grom games.ini
    



if __name__ == '__main__':
  a = Game(None, 'strilej', 'strilej', 'abc@abc.abc')
  print 'Game gameid:', a.gameid
  print 'Game owner:', a.owner
  print 'Game round:', a.round
  print 'Game gamedir:', a.gamedir
  print 'Game strat1:', a.strat1
  print 'Game strat2:', a.strat2
  a.play(1)
  a.cleanup()
