#!/usr/bin/env bash

PWD=$(cd $(dirname $0);pwd)
# 1. train
python -u $PWD/learn_pcfg.py config_train model
# 2. parse:
python -u $PWD/cyk.py model parse