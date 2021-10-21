#!/bin/bash

vagrant up
vagrant ssh -- "cd /browserbench && ./lebench.py"