---
name: obsidian-canvas
description: Create and edit Obsidian .canvas files using the JSON Canvas format. Use when working with .canvas files, creating visual canvases, mind maps, flowcharts, project boards, knowledge graphs, or when the user wants to organize notes/content spatially. Triggers on requests for infinite canvas layouts, visual diagrams, node-and-edge visualizations, or Obsidian Canvas files.
---

# Obsidian Canvas Creator

Create .canvas files for Obsidian using the JSON Canvas open format.

## Quick Start

Minimal canvas with text nodes and a connection:

```json
{
  "nodes": [
    {
      "id": "8a9b0c1d2e3f4a5b",
      "type": "text",
      "text": "# Main Idea\n\nCore concept here",
      "x": 0,
      "y": 0,
      "width": 250,
      "height": 150
    },
    {
      "id": "1a2b3c4d5e6f7a8b",
      "type": "text",
      "text": "## Related Point",
      "x": 350,
      "y": 0,
      "width": 200,
      "height": 100
    }
  ],
  "edges": [
    {
      "id": "3c4d5e6f7a8b9c0d",
      "fromNode": "8a9b0c1d2e3f4a5b",
      "fromSide": "right",
      "toNode": "1a2b3c4d5e6f7a8b",
      "toSide": "left"
    }
  ]
}
```

**Newline Escaping:** Use `\n` for line breaks, NOT `\\n` (renders as literal backslash-n).

## Complete Specification

For all node types (text, file, link, group), edge attributes, colors, and validation rules, see [references/specification.md](references/specification.md).

## Layout Guidelines

**Positioning:**
- Position (`x`, `y`) = top-left corner of node
- `x` increases rightward, `y` increases downward
- Coordinates can be negative (infinite canvas)

**ID Generation:** Obsidian uses 16-char lowercase hex:
```python
import secrets
node_id = secrets.token_hex(8)  # "6f0ad84f44ce9c17"
```

**Spacing:** 50-100px between nodes for readability.

**Typical dimensions:**
- Text nodes: 250x150 to 400x300
- File nodes: 400x300 to 600x400
- Groups: Size to contain children with 50px padding

**Z-Index:** Nodes render in array order (first = bottom). Place groups before contained nodes.

**Grid layout:**
```python
x = col * 400  # horizontal spacing
y = row * 250  # vertical spacing
```

**Radial layout:**
```python
angle = (2 * pi * i) / node_count
x = center_x + radius * cos(angle)
y = center_y + radius * sin(angle)
```

## Python Helper Script

For programmatic canvas generation, use `scripts/create_canvas.py`:

```python
from scripts.create_canvas import CanvasBuilder

canvas = CanvasBuilder()
n1 = canvas.add_text_node("# Title", x=0, y=0)
n2 = canvas.add_text_node("Details", x=400, y=0)
canvas.add_edge(n1, n2)
canvas.save("output.canvas")
```

Key methods: `add_text_node()`, `add_file_node()`, `add_link_node()`, `add_group_node()`, `add_edge()`, `create_grid_layout()`, `create_radial_layout()`.

## Common Patterns

- **Mind map:** Central node with radial connections
- **Flowchart:** Vertical flow with decision branches and loopbacks
- **Timeline:** Horizontal sequence with left-to-right edges
- **Hierarchy:** Tree structure with top-down layout
- **Knowledge graph:** Densely connected network with labeled edges
- **Kanban board:** Groups as columns containing task cards

## Examples

See `examples/` for complete canvas samples:
- `simple-mindmap.canvas` - Hub-and-spoke structure
- `project-board.canvas` - Kanban with groups
- `knowledge-graph.canvas` - Cross-connected concepts
- `flowchart.canvas` - Decision flow with loopback
