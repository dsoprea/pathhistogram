#!/bin/bash -ex

python3 -m nose -s -v --with-coverage --cover-package=pathhistogram tests
