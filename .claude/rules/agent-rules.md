---
paths:
  - ".agents/rules/**/*"
  - ".claude/rules/**/*"
---

# Agent rule maintenance

Keep shared rule sources in `.agents/rules/` and define their scopes in
`.agents/scopes.json`. Generate Claude adapters from those sources; do not edit
generated `.claude/rules/` files directly. Keep rules focused and reference
canonical project documentation.
