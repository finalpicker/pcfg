#!/usr/bin/env bash

PWD=$(cd $(dirname $0);pwd)

chmod 777 $PWD/step_1:run.sh
chmod 777 $PWD/step_2:clean.sh

sh $PWD/step_1:run.sh
