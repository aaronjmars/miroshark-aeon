#!/usr/bin/env bash
# Temporary wrapper to invoke ./notify with the message body from
# .notify-msg.txt without depending on $(cat ...) substitution.
set -euo pipefail
cd /home/runner/work/miroshark-aeon/miroshark-aeon
MSG=$(cat .notify-msg.txt)
exec ./notify "$MSG"
