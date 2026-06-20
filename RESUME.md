# RESUME — borderlint (handoff state)

> Snapshot of where we are, so a resumed Claude session (or you) can pick up instantly.
> Generated 2026-06-20.

## What borderlint is
A static, developer-side CLI for **HK / GBA entities** that maps where an application's AI data and
traffic flow and governs them against a **data-residency policy**, in CI, before code ships. East-west
lens (Western + Tencent/Alibaba/DeepSeek/… treated evenly). MIT, vendor-neutral, solo OSS.
Full scope: **`CAPABILITIES.md`**.

## Current state ✅
- **Spec-driven workflow adopted**: `opsx` + OpenSpec scaffolded (Claude target, `work_mode: flexible`, no Jira). See `AGENTS.md`, `workflow.yaml`, `openspec/config.yaml` (stack recorded).
- **P1 spec written, reviewed, and APPROVED**:
  - Change: `openspec/changes/mvp-residency-scanner/` — `proposal.md`, `design.md`, four capability specs (`flow-detection`, `jurisdiction-classification`, `residency-policy`, `cli-and-reporting`), `tasks.md` (6 groups, ~26 steps).
  - `openspec validate mvp-residency-scanner --strict` → **valid**.
  - `spec-reviewer` gate → **APPROVE** (after one revision cycle that added provider allow/deny, configurable failure-set, and home-regime, plus de-dup + unknown-warn scenarios).
- **No implementation code yet — by design.**

## NEXT STEPS (where to pick up)
1. **Commit the approved spec** as a checkpoint: `docs(spec): mvp-residency-scanner P1 spec`.
2. **Create the working branch**: `git checkout -b feature/mvp-residency-scanner` (repo has no commits yet; `main` is the protected release branch).
3. **Build P1**: `/opsx-apply` — work through `tasks.md` group by group, committing per step (`/git-commit`, conventional commits traced to `Change:`/`Task:`).
4. When `tasks.md` is all green: `/ship` (flexible mode → validate, archive the change into `openspec/specs/`, no PR).

## Locked design decisions (don't relitigate)
- **Policy = user-provided JSON eval-set**: data classification (`non-pii` | `employee-pii` | `customer-pii`, extensible) → allow-list of jurisdictions. Per-run `--classification` declares the data class on the scanned path.
- **Jurisdictions = ccTLD/ISO country codes** (lowercase `hk`, `cn`, `sg`, `my`, `us`, `gb`, `mo`, …) **plus special tokens `CN-GBA`** (nine Mainland GBA cities) **and `GBA`** (= `hk` + `CN-GBA`). **Deny-by-default** — no `overseas` grab-bag. This encodes a PDPO agreed-locations EULA (e.g. allow `sg`, not `my`, for customer PII).
- **Regimes (v1)**: PDPO (HK), PIPL (Mainland/GBA), GBA Standard Contract. User declares home regime; it selects which arrangement reference links are surfaced. Arrangements are **reference links only, never adjudicated**.
- **Scope**: v1 is for HK/GBA home bases only (not global). Out of v1: TypeScript scanning, SARIF, GitHub Action, LLM enrichment, per-city CN-GBA resolution, supply-chain/container SCA mode.

## Tooling notes (on clawbase)
- This repo is native here (`~/borderlint`). Ensure CLIs are on PATH: `npm i -g @fission-ai/openspec` (need Node ≥18; have 22). `opsx` is invoked via `npx @davidpv/opsx@latest`.
- Verify: `openspec validate mvp-residency-scanner --strict` and `openspec status --change mvp-residency-scanner`.

## Session migration
- This conversation's transcript + project memories were staged at:
  `~/.claude/projects/-home-iolaire-borderlint/` (the `.jsonl` + `memory/`).
- Resume: `cd ~/borderlint && claude --resume 91103182-7e49-4612-8c22-f07951e56391`
