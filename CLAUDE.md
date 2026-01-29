# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

A collection of custom skills for Claude Code. Skills extend Claude's capabilities with specialized knowledge and workflows. Currently contains the `obsidian-canvas` skill for creating Obsidian .canvas files.

## Skill Structure

Each skill follows this structure:
```
skill-name/
├── SKILL.md           # Skill definition with YAML frontmatter (name, description)
├── references/        # Supporting documentation and specifications
├── examples/          # Sample outputs demonstrating the skill
└── scripts/           # Helper scripts (optional)
```

The YAML frontmatter in SKILL.md defines how Claude Code discovers and triggers the skill:
```yaml
---
name: skill-name
description: When to use this skill...
---
```

## Installation for Testing

Symlink a skill to test it locally:
```bash
ln -s "$(pwd)/obsidian-canvas" ~/.claude/skills/obsidian-canvas
```

Or copy for permanent installation:
```bash
cp -r obsidian-canvas ~/.claude/skills/
```

## Python Helper (obsidian-canvas)

The `obsidian-canvas/scripts/create_canvas.py` provides a `CanvasBuilder` class for programmatic canvas generation:

```bash
# Run directly to create example canvas
python obsidian-canvas/scripts/create_canvas.py --example mindmap -o output.canvas

# Or import in scripts
from scripts.create_canvas import CanvasBuilder
```

No external dependencies required—uses only Python standard library.

## Canvas File Format

- `.canvas` files are JSON with `nodes` and `edges` arrays
- Node IDs are 16-character lowercase hex (use `secrets.token_hex(8)`)
- Use `\n` for newlines in text, NOT `\\n`
- Groups must appear before contained nodes in the array (z-index ordering)
