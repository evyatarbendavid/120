---
title: Find which GitHub repos are completely empty
tags: github, empty, repo, size
saved: 2026-10-31
---

# Find which GitHub repos are completely empty

## Problem
Need to know which of the owner's repos have no commits at all.

## Solution
For each repo: gh api repos/<owner>/<repo> --jq .size (0 for empty), gh api repos/<owner>/<repo>/branches --jq length (0), and gh api repos/<owner>/<repo>/contents answers 404 'This repository is empty.'. Private repos need add_repo first. For public repos: git ls-remote <url> prints nothing when empty.

## How to check it worked
All three checks agree for each repo reported empty.
