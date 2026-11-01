# Project guidance

Audio Fingerprinter is a Python 3.14 Flask API that generates Chromaprint audio
fingerprints using `ffmpeg` and `fpcalc`. Read `README.md` for setup and API
behavior and `CONTRIBUTING.md` for Gitflow, validation and release procedures.

Before working on matching files, read the rule listed below. Paths are relative
to the repository root; `**/` includes files at the root. Claude `paths:`
metadata is not a Codex loader.

- For `.agents/rules/**/*` and `.claude/rules/**/*`, read `.agents/rules/agent-rules.md`.
- For `CHANGELOG.md`, read `.agents/rules/changelog.md`.
- For `**/*`, read `.agents/rules/contributing.md`.

Also consult the applicable rule when performing its associated activity, even
without editing a matching file. Edit shared sources and regenerate Claude
adapters with the [public agent-config repository](https://github.com/BehindTheMusicTree/agent-config)
at v1.1.0: from this project root run
`python3 /path/to/agent-config/scripts/render-project-rules.py . --apply`.

For local startup use the shared `.agents/skills/launch/SKILL.md` skill, linked
from `.claude/skills/launch`.
