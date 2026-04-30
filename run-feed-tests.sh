#!/bin/bash
set -e
cd /tmp/build-target/backend
exec python3 -m pytest "$@"
