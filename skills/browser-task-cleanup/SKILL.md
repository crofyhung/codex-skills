---
name: browser-task-cleanup
description: Finish Chrome, browser automation, Chrome extension, browser-use, control-chrome, store backend, admin console, marketplace, web research, testing, verification, or logged-in web tasks by cleaning up temporary tabs and tab groups before the final response. Use when a task opens or groups browser tabs, especially after ecommerce operations, account checks, publishing tests, topic validation, reference gathering, or any browser task that may leave unused pages behind.
---

# Browser Task Cleanup

## Overview

Keep the user's browser light after task work. Before finishing any browser-based task, review what was opened for the task, close temporary pages, remove temporary tab groups, and clearly tell the user what was kept and why.

## Cleanup Workflow

1. Identify task-related tabs and groups.
   - Include pages opened for research, testing, verification, admin checks, publishing flows, login checks, reference gathering, and screenshots.
   - Treat colored/named groups created for the task as temporary unless the user explicitly asked to keep them.

2. Decide what can be closed.
   - Close completed task pages, duplicate pages, stale verification tabs, search result pages, temporary docs, and unused tool tabs.
   - Delete temporary tab groups once their tabs are closed or no longer needed.
   - Prefer leaving the user's pre-existing personal tabs alone.

3. Keep important pages when needed.
   - Keep pages that are still needed for the next confirmed step.
   - Keep result pages the user should inspect, active compose/publish forms, payment or account pages, unfinished uploads, pages with unsaved changes, and hard-to-restore logged-in pages.
   - If unsure, keep the page and mention the reason in plain language.

4. Verify the browser state.
   - After cleanup, check that only useful tabs remain.
   - If a group remains, it should have a clear reason: active work, user review, or a page that would be risky to close.

5. Report the cleanup briefly.
   - Say that temporary tabs/groups were closed.
   - Name anything intentionally kept and why.
   - Use simple, non-technical language.

## Safety Rules

- Never close a tab with unsaved form input, an active upload, a payment/refund flow, account recovery flow, publishing draft, or unclear login state unless the user explicitly asks.
- Never close unrelated tabs that existed before the task unless the user asked for a general browser cleanup.
- When using the user's logged-in Chrome, be more conservative than with a disposable browser session.
- If browser control is unavailable, mention that cleanup could not be performed and explain the likely remaining tabs/groups.

## Final Response Pattern

Use a short note such as:

> I also cleaned up the temporary browser tabs/groups from this task. I kept [page/group] because [reason].
