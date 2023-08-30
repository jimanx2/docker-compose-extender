#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

function @compose {
    python3 $SCRIPT_DIR/compose-cmd.py "$@"
}

function docker {
    if [ "$1" = "compose" ]; then
        docker-compose "$@"
    else
        command docker "$@"
    fi
}
