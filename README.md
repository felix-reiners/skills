# Claude Code Skills

A collection of custom skills for [Claude Code](https://claude.ai/code), Anthropic's official CLI for Claude.

## Available Skills

### [obsidian-canvas](./obsidian-canvas/)

Create production-ready Obsidian `.canvas` files with intelligent layout handling.

**Key Features:**

- **Auto-sizing nodes** — Height is calculated from content to prevent text cutoff. No more truncated labels or clipped descriptions.

- **Row-aligned column layouts** — For flowcharts and pipelines, nodes in the same row automatically match the tallest node's height, keeping your diagram clean and readable.

- **Straight connector logic** — Explicit guidance for vertical (`bottom` → `top`) and horizontal (`right` → `left`) flows, so your arrows don't zigzag unnecessarily.

- **Python helper library** — Programmatically generate canvases with `CanvasBuilder`. Includes `estimate_height()` for content-aware sizing and `create_column_layout()` for multi-column flowcharts.

- **Smart file placement** — Defaults to `docs/` folder when it exists (common in dev projects), otherwise saves to vault root.

**Example use cases:**
- System architecture diagrams
- Data pipeline flowcharts
- Project documentation with linked notes
- Mind maps and knowledge graphs

## Installation

Copy the skill folder to your Claude Code skills directory:
```bash
cp -r obsidian-canvas ~/.claude/skills/
```

Or symlink for development:
```bash
ln -s "$(pwd)/obsidian-canvas" ~/.claude/skills/obsidian-canvas
```

## Usage

Once installed, Claude Code will automatically use these skills when relevant:

```
> Create a canvas showing my API authentication flow

> Make a flowchart for the data ingestion pipeline with 3 input sources

> Generate an architecture diagram for this project
```

## Structure

Each skill contains:
- `SKILL.md` — Skill definition with instructions for Claude
- `references/` — Supporting documentation and specifications
- `examples/` — Sample outputs demonstrating the skill
- `scripts/` — Helper scripts (Python utilities, etc.)

## Contributing

To add a new skill:
1. Create a new directory with your skill name
2. Add a `SKILL.md` file following the existing format
3. Include examples and any supporting files
4. Submit a pull request

## License

MIT — see [LICENSE](./LICENSE)
