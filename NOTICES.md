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
| `moneyprinterturbo-video` | [harry0703/MoneyPrinterTurbo](https://github.com/harry0703/MoneyPrinterTurbo) (`docs/skill/`: `SKILL.md` and `mpt_agent.py`). **Modified**: a "Local notes" section was appended to `SKILL.md` (Hebrew voices, no secrets in chat, free routes only, Windows/macOS only); everything above it is upstream text. | MIT |

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
- `ui-styling/scripts/.coverage` is a harmless leftover SQLite file from the upstream author.
