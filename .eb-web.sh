#!/bin/bash
if [ "$CONFIG_BASE64" != "" ]; then
    echo "using CONFIG_BASE64"
    set -a
    . <(echo $CONFIG_BASE64 | base64 -d)
    set -a
else
    echo "CONFIG_BASE64 empty"
fi

uvicorn main:app
