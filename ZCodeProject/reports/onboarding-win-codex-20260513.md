# Codex Onboarding Report

| Field | Value |
|---|---|
| device | win-codex |
| agent | codex |
| workspace | C:\Users\lk\ZCodeProject |
| Jeff1993 root | C:\Users\lk\Documents\Jeff1993 |
| date | 2026-05-13 |
| mode | apply local status only |

## Checks

- Read `C:\Users\lk\Documents\Jeff1993\collab-entry.md`.
- Read `C:\Users\lk\Documents\Jeff1993\onboarding.md` headings and protocol sections.
- Verified Jeff1993 root contains `collab-entry.md`, `onboarding.md`, `agent-kit`, and `.project-status.yaml`.
- Ran `git pull` for `C:\Users\lk\ZCodeProject`; repository is already up to date.
- Checked Codex skills under `C:\Users\lk\.codex\skills`; required onboarding/checkpoint-related skills are present.

## Rule Summary

- Start work by pulling latest state, viewing status, reading tasks, and updating own status file.
- Only modify this device's own status file under `status/`.
- Event logs are append-only.
- Secret payloads must not be written to Git; secret recovery is dry-run-first and explicit-confirmation-only.
- End work by marking status idle/done, appending completion event, updating tasks if applicable, then committing and pushing when requested by the protocol.

## Notes

- This workspace did not initially contain `status/`, `events/`, `TODO.md`, or `status/view.sh`.
- Created `status/win-codex.yaml` and `events/win-codex.log` for this Codex device.
- No project code was modified during onboarding.
