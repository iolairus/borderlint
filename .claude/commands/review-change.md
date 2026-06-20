---
description: Audit an OpenSpec change for traceability and spec quality
---

> Delegate this work to the `spec-reviewer` subagent (read-only reviewer) and relay its full report to the user.


Review the OpenSpec change `$ARGUMENTS` under `openspec/changes/`. Apply the full checklist (proposal traceability, requirement quality, delta correctness, plan coherence, scope) and run `openspec validate $ARGUMENTS --strict`. Give a verdict: APPROVE or REVISE.
