---
title: Private GitHub repo looks missing, or gh CLI is not active
tags: github, private, repo, add_repo, gh, 404, access
saved: 2026-10-31
---

# Private GitHub repo looks missing, or gh CLI is not active

## Problem
A repo of the owner's answers 404 / 'Repository not found', or gh api says it is not active or not allowed for that repo in a cloud session.

## Solution
Call the add_repo tool (owner, repo; access: push if you will write). Do not pre-check with curl or git ls-remote: private repos answer 404 to anonymous requests even when they exist. If gh is inactive, load the mcp__github__* tools with ToolSearch; for public repos git ls-remote https://github.com/<owner>/<repo>.git works without credentials. list_repos shows every repo the account can attach.

## How to check it worked
After add_repo, gh api repos/<owner>/<repo> or the GitHub MCP get_file_contents returns data.
