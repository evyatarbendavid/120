# Sources and licenses

Every skill in `.claude/skills/` is copied unmodified from the public repository named
below and keeps its original license. Full license texts are in `LICENSES/`, and per-skill
`LICENSE.txt` files are kept where the upstream ships them.

| Skills | Source | License |
|---|---|---|
| `ui-ux-pro-max`, `banner-design`, `brand`, `design`, `design-system`, `slides`, `ui-styling` | [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | MIT |
| `watch` | [bradautomates/claude-video](https://github.com/bradautomates/claude-video) | MIT |
| `no-ai-slop` | [petergyang/no-ai-slop](https://github.com/petergyang/no-ai-slop) | MIT |
| 98 AI/ML research skills | [orchestra-research/AI-research-SKILLs](https://github.com/orchestra-research/AI-research-SKILLs) | MIT |
| 49 marketing skills | [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) | MIT |
| ~276 engineering-pattern skills (`skills/` only; `design-system` was renamed `design-system-ecc`) | [affaan-m/ecc](https://github.com/affaan-m/ecc) | MIT |
| `frontend-design`, `algorithmic-art`, `brand-guidelines`, `canvas-design`, `claude-api`, `doc-coauthoring`, `internal-comms`, `mcp-builder`, `slack-gif-creator`, `theme-factory`, `web-artifacts-builder`, `webapp-testing`, `academy-guide`, `discernment-nudge` | [anthropics/skills](https://github.com/anthropics/skills) | Apache 2.0 |
| 21 HyperFrames skills (`hyperframes`, `hyperframes-*`, `media-use`, `motion-graphics`, `slideshow`, `product-launch-video`, ...) | [heygen-com/hyperframes](https://github.com/heygen-com/hyperframes) | Apache 2.0 |
| `ai-video-editing-workflow` | Original skill, written for this repository. Its principles are distilled from a practitioner's guide on AI video editing by Roy Shavit (2026) and rewritten in new words; no text or templates were copied. | Same as this repository |
| `hallmark` | [Nutlope/hallmark](https://github.com/Nutlope/hallmark) (`skills/hallmark`) | MIT |
| `avoid-ai-design` | [funboy322/avoid-ai-design](https://github.com/funboy322/avoid-ai-design) (skill, references and scanner; demo pages left out) | MIT |
| `humanizer` | [blader/humanizer](https://github.com/blader/humanizer) | MIT |
| `avoid-ai-writing` | [conorbronsdon/avoid-ai-writing](https://github.com/conorbronsdon/avoid-ai-writing) (skill, patterns, detector, helper scripts, examples) | MIT |
| 32 more ECC skills added 2026-10-18 (`agent-runtime-gateway-smoke-test`, `agent-security-hardening`, `bengali-nlp`, `brownfield-retrospective`, `change-impact`, `context-and-decisions`, `conventional-commit-review`, `counterparty-channel-discipline`, `deepseek-harness-setup`, `docs-governance`, `ecc-guide`, `esign-field-placement`, `fal-ai-media`, `i18n-sync`, `ito-baskets`, `ito-compute`, `ito-inference`, `ito-training`, `master-agreement-generator`, `mcp-dependency-review`, `module-regression`, `mybatis-patterns`, `operator-approval-loop`, `osint-investigation`, `prompt-caching-strategy`, `rails-patterns`, `skill-host-compat`, `story-lifecycle`, `taste-application`, `taste-distillation`, `test-collaboration`, `token-card`) | [affaan-m/ecc](https://github.com/affaan-m/ecc) (`skills/`) | MIT, except `osint-investigation`: CC-BY-SA-4.0 (adapted from shoyann/RZK-The-Hunter; its `LICENSE.txt` is kept) |
| 282 subagents in `.claude/agents/` (The Agency: engineering, design, marketing, sales, product, testing, security, game development, GIS, finance, academic and more) | [msitarzewski/agency-agents](https://github.com/msitarzewski/agency-agents) (the same files its installer copies for Claude Code) | MIT |
| `anatomy` | [wheresryan22/anatomy](https://github.com/wheresryan22/anatomy) (all tracked files, unmodified) | MIT |
| `chief-of-staff` | [mimurchison/claude-chief-of-staff](https://github.com/mimurchison/claude-chief-of-staff). The repo is a set of commands and templates, not a skill: it is kept unmodified in `chief-of-staff/upstream/`, and `SKILL.md` is a new wrapper written here that says how to run it and forbids running `install.sh` (it overwrites `~/.claude/CLAUDE.md`). | MIT |
| `marketing-psychology-borghei` | [borghei/Claude-Skills](https://github.com/borghei/Claude-Skills) (`marketing/marketing-psychology`). **Modified**: folder and `name` renamed from `marketing-psychology` so it does not collide with the coreyhaines31 skill of that name. | MIT with the Commons Clause (free to use and share; may not be sold), `LICENSE` kept in the folder |
| `open-social-link` | Original skill, written for this repository (yt-dlp + ffmpeg + local faster-whisper; a helper that makes the browser trust the cloud proxy). | Same as this repository |
| 37 Vercel skills (`ai-sdk`, `vercel-cli`, `deployments-cicd`, `vercel-functions`, `vercel-storage`, `workflow`, `chat-sdk`, `react-best-practices`, ...) and 3 agents (`ai-architect`, `deployment-expert`, `performance-optimizer`) | [vercel/vercel-plugin](https://github.com/vercel/vercel-plugin) (`skills/`, `agents/*.md`), unmodified | Apache 2.0 |
| `seedance-prompt` | Written by the owner and added verbatim at their request. | Same as this repository |
| `ig-account-insights` | Original skill, written for this repository: the owner's own Instagram account through Meta's official read-only API or the account's data export. No passwords, no unofficial login. | Same as this repository |
| `product-sourcing` | Original skill, written for this repository: public listing search on Alibaba, AliExpress, Amazon and eBay, plus margin and supplier vetting. No login, no purchases. | Same as this repository |
| `reel-edit-hooks` | Original skill, written for this repository. It points to `ig-reel` and `ai-video-editing-workflow` and copies nothing from them. | Same as this repository |
| `moneyprinterturbo-video` | [harry0703/MoneyPrinterTurbo](https://github.com/harry0703/MoneyPrinterTurbo) (`docs/skill/`: `SKILL.md` and `mpt_agent.py`). **Modified**: a "Local notes" section was appended to `SKILL.md` (Hebrew voices, no secrets in chat, free routes only, Windows/macOS only); everything above it is upstream text. | MIT |
| 13 Instagram skills: `ig-reel` (26 hook formulas in `hooks.json`, hook scorer, beat sheet), `ig-viral`, `ig-caption`, `ig-carousel`, `ig-story`, `ig-profile`, `ig-plan`, `ig-comment`, `ig-reply`, `ig-dm`, `ig-repurpose`, `ig-audit`, `ig-human` | [Jakeschincariol/instagram-agent-skill](https://github.com/Jakeschincariol/instagram-agent-skill) (`skills/`; the voice template is in `templates/instagram-voice.md`) | MIT |

## Security review (2026-10-13)

All skills were scanned statically with `scripts/scan-skills.py` (nothing was executed): hooks and
settings wiring, download-and-run, obfuscation, credential access, exfiltration channels, destructive
commands, prompt-injection phrases, hidden Unicode, secrets, binaries, syntax of every script and JSON file.
Result: no hooks, no secrets, no obfuscated code, no binaries other than one shadcn tarball
(`web-artifacts-builder`, 49 plain entries, no absolute paths or links), no corrupted files. Behaviours worth knowing:

- `media-use` (HyperFrames) sends anonymous usage telemetry to PostHog (media type, source and provider; no
  text, names or paths; linked to the HeyGen account email only when signed in to HeyGen). It prints a notice
  once. Opt out with `DO_NOT_TRACK=1` or `HYPERFRAMES_NO_TELEMETRY=1`.
- `watch` uploads the extracted audio to Groq or OpenAI only when `GROQ_API_KEY` or `OPENAI_API_KEY` is set. It
  pre-approves the `Bash` tool while the skill is active.
- `council-multi-model` sends a review packet to OpenAI only with an explicit `--consent-to-openai`, and gives the
  subprocess a minimal environment.
- `avoid-ai-design` can optionally run as a PostToolUse hook (`detect.mjs --hook`); nothing installs it.
- `moneyprinterturbo-video` downloads the upstream `main` branch on first use and runs its code and its
  dependencies, installs `uv` through the official installer if missing, and prints sponsor links.
- Documentation inside `unsloth` and `axolotl` shows the official `curl | sh` installers for `uv` and Ollama.
  They are text only; nothing runs them.
- The `ig-*` skills (added 2026-10-18) use only the Python standard library: no network, no installs, and they write only to a path the user names. `ig-reel/hooks.json` is a list of video hook formulas, not Claude Code hooks. The skills never log in to Instagram, never post and never automate comments or DMs. The scorers are tuned for English: Hebrew text runs without errors but scores lower than it should, so treat those scores as rough.
- ECC skills still left out on purpose, because they install automatic hooks that run on every tool call or session: `ck`, `continuous-learning`, `continuous-learning-v2`, `delivery-gate`, `gateguard`, `inherit-legacy-style`, `plankton-code-quality`, `safety-guard`, `strategic-compact`. `fal-ai-media` and the four `ito-*` skills are in, but they only do anything with a paid account and its key. `token-card` runs the npm package `@tokenchit/cli` when used.
- ECC update check (2026-10-18, upstream 76aaa77): 302 ECC skills compared, 200 unchanged, 71 updated to upstream (each one grew and kept every section). 31 were held back because the upstream version is shorter or drops sections, and skills here are never shrunk without the owner asking: `accessibility`, `api-design`, `autonomous-agent-harness`, `blueprint`, `bun-runtime`, `carrier-relationship-management`, `competitive-platform-analysis`, `configure-ecc`, `context-budget`, `cost-aware-llm-pipeline`, `customs-trade-compliance`, `dart-flutter-patterns`, `ecc-recipes`, `ecc-tools-cost-audit`, `energy-procurement`, `flox-environments`, `github-ops`, `inventory-demand-planning`, `logistics-exception-management`, `loop-design-check`, `orch-build-mvp`, `plan-orchestrate`, `production-scheduling`, `prompt-optimizer`, `quality-nonconformance`, `returns-reverse-logistics`, `skill-scout`, `taste`, `tasteforge-video`, `token-budget-advisor`, `videodb`.
- The agency-agents subagents (added 2026-10-18) are plain instructions with no scripts. 265 of them inherit every tool when called; 17 list their tools. Six list outside services they can use (free tiers or the user's own API keys). Hits from the scan are security-education text: a list of secret patterns to detect, and attack names in the security agents.
- Added 2026-10-18 after review: `anatomy` (no dependencies; its scripts start a local headless Chrome for checks and talk to it on 127.0.0.1; `scripts/publish.mjs` reads the current Claude Code session log only to count minutes and tokens for a gallery entry, and pushes nothing without `--submit` plus a confirmation; 254 of 259 of its own tests pass here, the other 5 need TypeScript, a development dependency), `chief-of-staff` (instructions and templates only; never sends without approval), `marketing-psychology-borghei` (three standard-library scripts, no network). `thebuggeddev/anatomy` was not added: it is a web app (a 3D organ viewer), not a skill, and it has no license, so it cannot be redistributed here.
- vercel-plugin (added 2026-10-22): only its skills and agents are here. Its `hooks/` are left out on purpose: they register themselves on every session start and tool call, inject context, and send skill-usage telemetry to telemetry.vercel.com. Its four commands (`/deploy`, `/env`, `/status`, `/bootstrap`) are left out because those generic names would sit in every repo; the `bootstrap` and deployment skills cover the same ground. The Vercel MCP server is already a claude.ai connector.
- `ui-styling/scripts/.coverage` is a harmless leftover SQLite file from the upstream author.
