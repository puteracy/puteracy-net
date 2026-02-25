#!/bin/bash

/etc/init.d/fcgiwrap start
nginx -g 'daemon off;'
