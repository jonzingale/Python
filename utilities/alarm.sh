#!/usr/bin/env bash

TARGET_HOUR=7
TARGET_MIN=0

# Current time components
now_h=$(date +%H)
now_m=$(date +%M)
now_s=$(date +%S)

# Compute seconds from midnight for now and for target
now_sec=$(( 10#$now_h * 3600 + 10#$now_m * 60 + 10#$now_s ))
target_sec=$(( TARGET_HOUR * 3600 + TARGET_MIN * 60 ))

# If target time already passed today, schedule for tomorrow
if [ "$target_sec" -le "$now_sec" ]; then
  target_sec=$(( target_sec + 24*3600 ))
fi

sleep_sec=$(( target_sec - now_sec ))

echo "Alarm set for next 7:00 AM. Sleeping for ${sleep_sec} seconds..."
sleep "${sleep_sec}"

# Alarm action: pick any one of these or customize
afplay /System/Library/Sounds/Glass.aiff 2>/dev/null || \
osascript -e 'display notification "Wake up!" with title "Alarm"' || \
printf '\a\nWAKE UP! It is 7:00 AM.\n'

# Alarm action: open Solarbridge YouTube page in default browser
URL="https://www.youtube.com/watch?v=ISG4YwnikJ0"

# Alarm action: play local MP3 track
SONG="$HOME/Desktop/music/MetroSync 08-02-1997/Is Chicago Is Not Chicago.aif"

# First try local *.aif, then YouTube Solarbridge, else fail with sound.
if [ -f "$SONG" ]; then
  echo "Playing alarm track: $SONG"
  afplay "$SONG"
else
  open "$URL" || {
    echo "Failed to open URL, falling back to system sound"
    afplay /System/Library/Sounds/Glass.aiff 2>/dev/null || \
    printf '\a\nWAKE UP! It is 7:00 AM.\n'
  }
fi
