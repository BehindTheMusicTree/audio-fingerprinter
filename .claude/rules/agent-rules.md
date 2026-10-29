---
description: Agent rules location and format standards
paths:
  - ".claude/rules/**/*"
---

# Agent Rules Standards

## Location

- Agent rules must be stored in the `.claude/rules/` directory

## File Format

- Use the `.md` file extension
- Frontmatter: `description`, plus `paths` for rules scoped to specific files (omit `paths` for always-loaded rules)
- Frontmatter format:
  ```yaml
  ---
  description: Brief summary of rule purpose
  paths:
    - "CHANGELOG.md"
  ---
  ```

## Organization

- Create focused, single-purpose rule files
- Name files descriptively (e.g., `contributing.md`, `changelog.md`)
- Reference main documentation files rather than duplicating content
- Keep rules concise and actionable
