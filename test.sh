#!/bin/sh

score=0

export OPENSHIFT_REPO_DIR='./'

echo "# Strategies"
libs/strategies.py
score+=$?

echo "# Games"
libs/games.py
score+=$?

echo "# Users"
cp data/users.csv{,.ORIG}
:> data/users.csv
libs/users.py
score+=$?
cp data/users.csv{.ORIG,}

echo "# RESULTS"
[ $score -ne 0 ] && echo "FAIL, error happened :-(" || echo "PASS :-)"
exit $score
