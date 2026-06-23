---
name: computer-use-session-hygiene
description: Prevent oversized Codex Desktop sessions for Computer Use-heavy work. Use when a task relies on Computer Use, desktop app automation, merchant/admin backends, screenshots, accessibility trees, DOM/page snapshots, recurring monitors, background UI work, large rollout JSONL files, Base64 images, "Invalid string length", session bloat, Codex diagnostic log write bloat, logs_2.sqlite growth, or when designing a new long-running project that will use Computer Use often.
---

# Computer Use Session Hygiene

Use this skill to make Computer Use sustainable for long-running projects. The goal is not to avoid Computer Use; the goal is to prevent screenshots, Base64 images, accessibility trees, DOM dumps, long logs, and Codex diagnostic logs from becoming the project's memory system.

## Default Rule

Treat Computer Use screenshots and UI trees as temporary working material.

Persist only:

- current task state
- durable operating rules
- key data read from the screen
- what changed or explicitly did not change
- output file paths
- next safe action and confirmation phrase

Do not persist:

- Base64 images
- repeated screenshots
- full accessibility trees
- full DOM / HTML dumps
- long raw logs
- entire scanned directories
- full historical transcripts in `current.md` or task `brief.md`

## Project Setup

When a project will use Computer Use repeatedly:

1. Ensure the project has `.codex-memory/`.
2. Create or update a stable rule file such as `.codex-memory/spec/codex-session-size-rules.md`.
3. Keep `.codex-memory/current.md` as a light entry point, not a timeline.
4. Keep active task `brief.md` files as summaries, not logs.
5. Put detailed work products in `output/` or task-specific files.
6. Put old or verbose history in `.codex-memory/archive/`.

Recommended size targets:

- `current.md`: about `10KB` or less.
- active task `brief.md`: about `20KB` or less.
- if either file grows beyond that, archive history and rewrite a light summary.

## Computer Use Work Blocks

Split UI automation into short work blocks:

- read the screen once to orient
- execute a small batch
- re-read only after navigation, uncertainty, or error
- write a compact result
- stop or switch threads before the session grows too much

Suggested batch size:

- read-only checks: `1-3` items per block
- risky real actions: one object/action per confirmation
- recurring monitors: one focused check per wakeup
- recovery attempts: at most two low-risk retries before stopping and reporting

## Session Size Guardrails

Use these thresholds for Codex session JSONL files:

- `100MB`: warning. Sync project memory and recommend a fresh chat.
- `250MB`: danger. Stop adding Computer Use work to that chat.
- `1GB` or `Invalid string length`: emergency. Do not load the file directly; use streaming reads and create a slim copy.

## Log Write Guardrails

Also watch Codex diagnostic logs during Computer Use-heavy work. This is separate from session JSONL bloat: session files can grow from screenshots, while `logs_2.sqlite` can create heavy SSD writes when Codex records too many internal events.

Check log write rate when:

- starting long Computer Use work
- starting recurring monitors, duty checks, or background automation
- multiple agents are running at the same time
- Chrome, Computer Use, MCP, or other tools repeatedly disconnect or retry
- Codex becomes slow, switches threads slowly, or feels stuck
- ending a long automation phase

Watch:

- `$CODEX_HOME/logs_2.sqlite`
- `$CODEX_HOME/logs_2.sqlite-wal`
- `$CODEX_HOME/sqlite/logs_2.sqlite`
- `$CODEX_HOME/sqlite/logs_2.sqlite-wal`

Suggested thresholds over a `60s` sample:

- normal: little or no growth
- warning: more than `10MB/min` growth or more than `2000` new rows/min
- danger: more than `50MB/min` growth or more than `10000` new rows/min
- emergency: sustained multi-MB/second growth, a log DB above `1GB` that is still growing, or repeated UI stalls tied to log writes

Response:

- warning: reduce status chatter, avoid repeated screenshots/UI trees, stop unnecessary background loops, then recheck
- danger: pause long Computer Use work, stop retry loops, sync project memory, and recommend a fresh chat or Codex restart
- emergency: quit Codex, back up logs, then consider clearing logs or applying a reviewed write-block workaround

Use:

```bash
${CODEX_HOME:-$HOME/.codex}/skills/computer-use-session-hygiene/scripts/codex-log-write-health.zsh
```

Run the health check when:

- the user asks about bloat, crashes, or `Invalid string length`
- a Computer Use project starts or resumes
- before ending a long Computer Use phase
- before creating recurring monitors
- when a project has used screenshots heavily

Use:

```bash
${CODEX_HOME:-$HOME/.codex}/skills/computer-use-session-hygiene/scripts/project-session-hygiene.zsh /path/to/project
```

## Reporting Pattern

For Computer Use work, report in this shape:

```text
本轮检查/执行：
- 页面/对象：
- 读到的数据：
- 做了什么：
- 没有动什么：
- 结果文件：
- 下一步：
```

Avoid step-by-step screenshot narration unless the user explicitly asks and the evidence is worth the session size cost.

## Recovery Pattern

If a session is already oversized:

1. Preserve the original file in a backup/quarantine location.
2. Never use whole-file reads on huge JSONL.
3. Prove what is large before changing anything. Count top record types, image payload paths, and tool names.
4. Use streaming line-by-line processing.
5. Default to Computer Use-only slimming: replace screenshots from Computer Use tool outputs and Computer Use MCP event logs.
6. Keep user/assistant text, compacted summaries, turn context, key metadata, project decisions, output paths, and task results.
7. Do not remove user-uploaded images or non-Computer Use images by default.
8. Validate the slim copy before calling it recovered.

Use the safe slimmer:

```bash
${CODEX_HOME:-$HOME/.codex}/skills/computer-use-session-hygiene/scripts/slim-computer-use-session.py \
  /path/to/original.jsonl \
  --dry-run
```

Then write to a new file:

```bash
${CODEX_HOME:-$HOME/.codex}/skills/computer-use-session-hygiene/scripts/slim-computer-use-session.py \
  /path/to/original.jsonl \
  --output /path/to/slim.jsonl \
  --validate
```

The script is intentionally conservative. It replaces Computer Use screenshots with a legal 1x1 transparent PNG placeholder and preserves non-Computer Use images unless explicitly handled by a future, reviewed option.

## New Project Rule

For any new project expected to use Computer Use often, create the session-size rule before the first long automation run. Do not wait for the first oversized file.

