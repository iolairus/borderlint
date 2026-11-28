# Backlog

This directory holds product discovery and task records that come before an OpenSpec change.
The workflow is:

```text
discovery/  →  tasks/  →  openspec/changes/  →  code
(/req-capture) (/task-generate, /task-enrich)  (/opsx-propose)
```

| Directory | Contents |
|---|---|
| `discovery/` | Requirements-gathering notes, one file per topic (`/req-capture`) |
| `tasks/` | Tasks named `<jira-key>-<slug>.md`, with traceability in frontmatter (`/task-generate`) |
| `exports/jira/` | Jira-ready versions of tasks (`/task-jira`) |
| `exports/pr/` | Pull-request descriptions used when no platform CLI is available (`/pr-open`) |

Task IDs are Jira keys in the form `<project_key>-<n>`, supplied by the user. Use
`<project_key>-Dnn` for a draft until the real issue exists.

A task's frontmatter tracks its `status` and `change`. Commands update these fields. Do not edit
them by hand unless you are correcting outdated information.
