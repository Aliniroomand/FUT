#!/usr/bin/env bash
# scripts/test_futbin_fetch.sh
# Usage: ./scripts/test_futbin_fetch.sh <player_id> [platform]
PLAYER=${1:-12345}
PLATFORM=${2:-pc}
curl -s "http://localhost:8000/futbin/price?player_id=${PLAYER}&platform=${PLATFORM}&ttl=3" | jq .
