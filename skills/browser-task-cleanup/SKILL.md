---
name: browser-task-cleanup
description: Manage Chrome/browser tab hygiene for browser-heavy tasks. Use when a task involves Chrome, browser automation, Chrome extension work, browser-use, control-chrome, Amazon Seller Central, Amazon Ads, SellerSprite or other ecommerce/data tools, store backend, admin console, marketplace pages, web research, testing, verification, logged-in web tasks, or any task likely to open temporary tabs. Record the pre-task browser state when possible, then clean up temporary tabs and tab groups before the final response while protecting risky ecommerce/admin pages.
---

# Browser Task Cleanup

## Overview

Keep the user's browser light after task work. Before finishing any browser-based task, review what was opened for the task, close temporary pages, remove temporary tab groups, and clearly tell the user what was kept and why.

## Start-of-Task Baseline

When browser control is available near the start of a browser-heavy task:

1. Capture or note the current browser tabs/groups before opening new pages.
2. Treat those pre-existing tabs as the user's tabs unless the user asks for a broader cleanup.
3. If the skill is loaded after work has already started, infer task-created pages from the conversation, page purpose, timestamps, tab groups, and navigation trail. When unsure, keep the tab.

## Cleanup Workflow

1. Identify task-related tabs and groups.
   - Include pages opened for research, testing, verification, admin checks, publishing flows, login checks, reference gathering, and screenshots.
   - Include Amazon product pages, search result pages, competitor pages, SellerSprite/data-tool pages, ad-console checks, listing checks, and duplicate marketplace pages opened only for the task.
   - Treat colored/named groups created for the task as temporary unless the user explicitly asked to keep them.

2. Decide what can be closed.
   - Close completed task pages, duplicate pages, stale verification tabs, search result pages, temporary docs, and unused tool tabs.
   - Delete temporary tab groups once their tabs are closed or no longer needed.
   - Prefer leaving the user's pre-existing personal tabs alone.

3. Keep important pages when needed.
   - Keep pages that are still needed for the next confirmed step.
   - Keep result pages the user should inspect, active compose/publish forms, payment or account pages, unfinished uploads, pages with unsaved changes, and hard-to-restore logged-in pages.
   - For Amazon Seller Central, Amazon Ads, store backends, publishing drafts, listing edit pages, bulk upload pages, report exports, payment/account/login/security pages, and any page showing a live operation in progress, keep the page unless the user explicitly said it can be closed.
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
- For heavy ecommerce/admin pages, prefer keeping risky tabs and explaining why over closing aggressively.
- If a task needs evidence review, screenshots, or the user's next manual action, keep that page and close the surrounding temporary research tabs.
- If browser control is unavailable, mention that cleanup could not be performed and explain the likely remaining tabs/groups.

## Final Response Pattern

Use the user's language. For Chinese owner/operator workflows, add one short plain-language cleanup note that says:

- Temporary browser pages opened for this task were cleaned up.
- Any kept page/group is named with the business reason it was kept.
