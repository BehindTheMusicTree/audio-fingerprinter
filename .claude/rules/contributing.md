---
paths:
  - "**/*"
---

# Contributing practices

Follow `CONTRIBUTING.md` for Gitflow, validation and PR requirements. Feature
and chore branches start from and target `develop`; release and hotfix workflows
are documented there. Do not commit directly to `main` or `develop`.

Use Python 3.14 and the existing code style. For API or configuration changes,
update the README and environment templates as appropriate. Run the documented
pytest coverage command for relevant changes.
