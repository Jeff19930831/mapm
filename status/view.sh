#!/bin/bash
# MAPM Global Status Viewer
# Usage: bash status/view.sh

set -e

STATUS_DIR="$(cd "$(dirname "$0")" && pwd)"
EVENTS_DIR="$(cd "$(dirname "$0")/../events" && pwd)"

# Column widths
W_DEVICE=15
W_AGENT=15
W_TASK=20
W_STATUS=12
W_UPDATED=20

# Print header
printf "\n====== Device Status ======\n\n"
printf "%-${W_DEVICE}s  %-${W_AGENT}s  %-${W_TASK}s  %-${W_STATUS}s  %-${W_UPDATED}s\n" \
    "DEVICE" "AGENT" "TASK" "STATUS" "UPDATED"
printf "%${W_DEVICE}s  %${W_AGENT}s  %${W_TASK}s  %${W_STATUS}s  %${W_UPDATED}s\n" \
    "$(printf '%*s' "$W_DEVICE" '' | tr ' ' '-')" \
    "$(printf '%*s' "$W_AGENT" '' | tr ' ' '-')" \
    "$(printf '%*s' "$W_TASK" '' | tr ' ' '-')" \
    "$(printf '%*s' "$W_STATUS" '' | tr ' ' '-')" \
    "$(printf '%*s' "$W_UPDATED" '' | tr ' ' '-')"

# Find and sort status files
files=()
while IFS= read -r -d '' f; do
    files+=("$f")
done < <(find "$STATUS_DIR" -maxdepth 1 -name '*.yaml' -print0 2>/dev/null | sort -z)

if [ ${#files[@]} -eq 0 ]; then
    printf "\nNo devices registered\n"
else
    for f in "${files[@]}"; do
        [ "$(basename "$f")" = "TEMPLATE.yaml" ] && continue

        device=$(grep '^device:' "$f" 2>/dev/null | head -1 | sed 's/device: *//' | tr -d '"' || echo '-')
        agent=$(grep '^agent:' "$f" 2>/dev/null | head -1 | sed 's/agent: *//' | tr -d '"' || echo '-')
        task=$(grep '^task:' "$f" 2>/dev/null | head -1 | sed 's/task: *//' | tr -d '"' || echo '-')
        status=$(grep '^status:' "$f" 2>/dev/null | head -1 | sed 's/status: *//' | tr -d '"' || echo '-')
        updated=$(grep '^updated:' "$f" 2>/dev/null | head -1 | sed 's/updated: *//' | tr -d '"' || echo '-')

        # Truncate and pad
        device="${device:0:$W_DEVICE}"
        agent="${agent:0:$W_AGENT}"
        task="${task:0:$W_TASK}"
        status="${status:0:$W_STATUS}"
        updated="${updated:0:$W_UPDATED}"

        # Replace empty with -
        [ -z "$device" ] && device='-'
        [ -z "$agent" ] && agent='-'
        [ -z "$task" ] && task='-'
        [ -z "$status" ] && status='-'
        [ -z "$updated" ] && updated='-'

        printf "%-${W_DEVICE}s  %-${W_AGENT}s  %-${W_TASK}s  %-${W_STATUS}s  %-${W_UPDATED}s\n" \
            "$device" "$agent" "$task" "$status" "$updated"
    done
fi

# Recent events
printf "\n\n====== Recent Events ======\n\n"

if [ ! -d "$EVENTS_DIR" ] || [ -z "$(ls -A "$EVENTS_DIR" 2>/dev/null)" ]; then
    printf "No events yet\n"
else
    # Collect last 5 lines from all log files, sort by timestamp, take last 5
    find "$EVENTS_DIR" -maxdepth 1 -name '*.log' -exec tail -n 5 {} + 2>/dev/null | \
        grep '^\[' | sort | tail -n 5 || printf "No events yet\n"
fi

printf "\n"
exit 0
