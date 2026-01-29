# Claude Code Skills

A collection of custom skills for [Claude Code](https://claude.ai/code), Anthropic's official CLI for Claude.

## Available Skills

| Skill | Description |
|-------|-------------|
| [obsidian-canvas](./obsidian-canvas/) | Create and edit Obsidian .canvas files using the JSON Canvas format. Supports mind maps, flowcharts, project boards, and knowledge graphs. |

## Installation

1. Copy the skill folder to your Claude Code skills directory:
   ```bash
   cp -r obsidian-canvas ~/.claude/skills/
   ```

2. Or symlink for development:
   ```bash
   ln -s "$(pwd)/obsidian-canvas" ~/.claude/skills/obsidian-canvas
   ```

## Usage

Once installed, Claude Code will automatically use these skills when relevant. For example:
- Ask Claude to "create an Obsidian canvas for my project structure"
- Request "make a mind map canvas showing the relationships between these concepts"

## Structure

Each skill contains:
- `SKILL.md` - The skill definition with instructions for Claude
- `references/` - Supporting documentation and specifications
- `examples/` - Sample outputs demonstrating the skill
- `scripts/` - Helper scripts (optional)

## Contributing

To add a new skill:
1. Create a new directory with your skill name
2. Add a `SKILL.md` file following the existing format
3. Include examples and any supporting files
4. Submit a pull request

## License

MIT
