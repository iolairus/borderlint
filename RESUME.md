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
- **P1 BUILT** on branch `feature/mvp-residency-scanner`: `borderlint/` (`kb`, `detect`, `policy`, `report`, `cli`) + JSON knowledge base + examples + 6 passing tests. **Zero runtime deps** (stdlib only; KB is JSON, not YAML). Two commits (spec, then impl). `openspec validate --strict` ✓; all `tasks.md` boxes checked. Verified end-to-end (customer-pii scan → 3 FAIL, DashScope-intl→sg OK, exit 1).

## NEXT STEPS (where to pick up)
1. **Verify**: `python -m borderlint scan examples --policy examples/residency.json --classification customer-pii` → expect 3 FAIL / exit 1 (or `/opsx-verify mvp-residency-scanner`).
2. **Ship**: `/ship` — validate, archive the change into `openspec/specs/`, merge `feature/mvp-residency-scanner` → `main` (flexible mode, no PR).
3. **Then P2** (`CAPABILITIES.md`): SARIF + GitHub Action, TypeScript scanning, supply-chain/container SCA mode, optional Claude enrichment.

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
