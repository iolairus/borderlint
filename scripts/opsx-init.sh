#!/usr/bin/env bash
# opsx-init.sh — scaffold the OPSX spec-driven workflow into a target repo.
#
# The "approach" is just files Claude Code reads on startup:
#   AGENTS.md      — the rules (Spec -> Plan -> Code; never skip a stage)
#   .claude/       — slash commands, the spec-reviewer gate, OpenSpec skills
#   openspec/      — specs (source of truth) + in-flight changes
#   workflow.yaml  — branches / commit convention (edit per project)
# Drop them in a repo and any Claude session opened there follows the pipeline.
#
# Usage:   scripts/opsx-init.sh [--no-jira] [target-dir]   # target default: current dir
#   --no-jira   strip the Jira/backlog layer: omit the jira:/backlog: workflow.yaml
#               blocks, the task-*/req-capture/review-task commands, the task-reviewer
#               agent, and the discovery/task templates + backlog/ dirs. Leaves the
#               core loop: /opsx:propose -> spec-reviewer -> /opsx:apply -> /git-commit -> /ship.
# Source:  $OPSX_SOURCE, else the repo this script lives in (the parent of scripts/).

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC="${OPSX_SOURCE:-$(dirname "$SCRIPT_DIR")}"
DST="."
NOJIRA=0
for a in "$@"; do
  case "$a" in
    --no-jira) NOJIRA=1 ;;
    -*) echo "unknown option: $a" >&2; exit 2 ;;
    *) DST="$a" ;;
  esac
done

[ -d "$SRC/.claude" ] || { echo "error: scaffold source not found at $SRC — set OPSX_SOURCE" >&2; exit 1; }
mkdir -p "$DST"
echo "opsx-init: $SRC  ->  $DST"
[ "$NOJIRA" = 1 ] && echo "  (--no-jira: core loop only)"

# copy without overwriting anything that already exists
copy() { cp -r --update=none "$1" "$2" 2>/dev/null || cp -rn "$1" "$2"; }

# 1. commands + spec-reviewer gate + OpenSpec skills (project scope, shareable)
mkdir -p "$DST/.claude/commands" "$DST/.claude/agents" "$DST/.claude/skills"
copy "$SRC/.claude/commands/." "$DST/.claude/commands/"
copy "$SRC/.claude/agents/."   "$DST/.claude/agents/"
copy "$SRC/.claude/skills/."   "$DST/.claude/skills/"

# 2. rules + pipeline config (workflow.yaml is a TEMPLATE — edit it)
copy "$SRC/AGENTS.md" "$DST/AGENTS.md"
[ -f "$DST/CLAUDE.md" ] || printf '@AGENTS.md\n' > "$DST/CLAUDE.md"
if [ "$NOJIRA" = 1 ]; then
  # drop the top-level jira: and backlog: blocks
  [ -f "$DST/workflow.yaml" ] || \
    awk '/^[A-Za-z_]+:/ { skip = ($0 ~ /^(jira|backlog):/) } !skip' "$SRC/workflow.yaml" > "$DST/workflow.yaml"
else
  copy "$SRC/workflow.yaml" "$DST/workflow.yaml"
fi

# 3. templates (pr-description always; discovery/task only with the task layer)
mkdir -p "$DST/templates"
if [ "$NOJIRA" = 1 ]; then
  [ -f "$SRC/templates/pr-description.md" ] && copy "$SRC/templates/pr-description.md" "$DST/templates/"
else
  copy "$SRC/templates/." "$DST/templates/"
fi

# 4. OpenSpec skeleton (+ backlog unless --no-jira)
DIRS="openspec/specs openspec/changes/archive"
[ "$NOJIRA" = 1 ] || DIRS="$DIRS backlog/discovery backlog/tasks backlog/exports/jira backlog/exports/pr"
for d in $DIRS; do mkdir -p "$DST/$d"; [ -e "$DST/$d/.gitkeep" ] || : > "$DST/$d/.gitkeep"; done

# 5. with --no-jira, remove the task/Jira-layer commands + agent + templates
if [ "$NOJIRA" = 1 ]; then
  for c in req-capture task-generate task-enrich task-import task-new task-jira review-task; do
    rm -f "$DST/.claude/commands/$c.md"
  done
  rm -f "$DST/.claude/agents/task-reviewer.md" "$DST/templates/discovery.md" "$DST/templates/task.md"
fi

echo
echo "done. next:"
echo "  1. edit $DST/workflow.yaml   (main_branch / integration_branch / work_mode)"
echo "  2. (optional) cd $DST && npx -y @fission-ai/openspec update"
echo "  3. open $DST in Claude Code and run /start"
[ "$NOJIRA" = 1 ] && echo "  note: AGENTS.md still mentions optional discovery/task stages — ignore them; your loop is propose -> gate -> apply -> commit -> ship"
