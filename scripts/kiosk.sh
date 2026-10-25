#!/usr/bin/env bash
set -euo pipefail

URL="${1:-http://127.0.0.1:8080/?kiosk=1}"

exec chromium \
  --kiosk \
  --app="$URL" \
  --noerrdialogs \
  --disable-infobars \
  --disable-session-crashed-bubble \
  --autoplay-policy=no-user-gesture-required
