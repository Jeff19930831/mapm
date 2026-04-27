#!/bin/bash
# Auto-sync script for MAPM status files
# Runs: commit local changes, pull remote, push
# Handles rebase interruption and conflicts automatically

set -euo pipefail

REPO_DIR="${MAPM_REPO:-$(cd "$(dirname "$0")" && pwd)}"
cd "$REPO_DIR"

LOG_FILE="${REPO_DIR}/.planning/sync.log"
STATUS_DIR="${REPO_DIR}/status"
EVENTS_DIR="${REPO_DIR}/events"
SPECS_DIR="${REPO_DIR}/specs"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Check if we're in a git repo
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    log "ERROR: Not a git repository"
    exit 1
fi

# Check for rebase in progress
if [ -d "$(git rev-parse --git-path rebase-merge)" ] || [ -d "$(git rev-parse --git-path rebase-apply)" ] 2>/dev/null; then
    log "Rebase in progress, aborting and retrying..."
    git rebase --abort 2>/dev/null || true
fi

# Stash any non-status changes (shouldn't happen, but safety)
STASHED=false
if ! git diff --quiet HEAD 2>/dev/null; then
    git stash push -m "auto-sync-stash-$(date +%s)" -- "$STATUS_DIR" "$EVENTS_DIR" "$SPECS_DIR" "TODO.md" 2>/dev/null || true
    STASHED=true
fi

# Commit local changes if any
if ! git diff --quiet HEAD -- "$STATUS_DIR" "$EVENTS_DIR" "$SPECS_DIR" "TODO.md" 2>/dev/null; then
    log "Committing local changes..."
    git add "$STATUS_DIR" "$EVENTS_DIR" "$SPECS_DIR" "TODO.md" 2>/dev/null || true
    git commit -m "sync: auto-update status $(date +%Y%m%d-%H%M%S)" || true
fi

# Pull with rebase
log "Pulling remote changes..."
if ! git pull --rebase origin main 2>/dev/null && ! git pull --rebase origin master 2>/dev/null; then
    log "Pull failed, trying merge strategy..."
    git pull origin main 2>/dev/null || git pull origin master 2>/dev/null || {
        log "Pull failed completely, will retry next run"
        exit 0
    }
fi

# Handle conflicts (keep remote for status/events)
if git diff --name-only --diff-filter=U | grep -qE "^(status/|events/|specs/|TODO\.md)"; then
    log "Resolving conflicts (keep remote for status/events)..."
    git diff --name-only --diff-filter=U | while read -r file; do
        case "$file" in
            status/*|events/*|specs/*|TODO.md)
                log "  Keeping remote: $file"
                git checkout --theirs "$file"
                git add "$file"
                ;;
        esac
    done
    git rebase --continue 2>/dev/null || git commit -m "sync: resolve conflicts $(date +%Y%m%d-%H%M%S)" || true
fi

# Push
log "Pushing to remote..."
if git push origin HEAD 2>/dev/null; then
    log "Sync complete"
else
    log "Push failed (may need manual resolution)"
fi

# Restore stashed changes
if [ "$STASHED" = true ]; then
    git stash pop 2>/dev/null || true
fi
