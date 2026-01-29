---
name: obsidian-canvas
description: Create and edit Obsidian .canvas files using the JSON Canvas format. Use when working with .canvas files, creating visual canvases, mind maps, flowcharts, project boards, knowledge graphs, or when the user wants to organize notes/content spatially. Triggers on requests for infinite canvas layouts, visual diagrams, node-and-edge visualizations, or Obsidian Canvas files.
---

# Obsidian Canvas Creator

Create .canvas files for Obsidian using the JSON Canvas open format.

## File Location

**Default path:** Save canvas files to `docs/` folder if it exists, otherwise vault root.
- Check if `docs/` directory exists in the target location
- If yes: `docs/diagram-name.canvas`
- If no: `diagram-name.canvas` in vault root
- If location is ambiguous, ask the user where to save

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

**Z-Index:** Nodes render in array order (first = bottom). Place groups before contained nodes.

## Node Sizing (CRITICAL)

**Never let content get cut off.** Calculate height based on text content:

```python
def estimate_height(text: str, width: int = 250, base_height: int = 60) -> int:
    """Estimate node height to fit all content."""
    lines = text.split('\n')
    total_lines = 0
    chars_per_line = (width - 40) // 8  # ~8px per char, 20px padding each side

    for line in lines:
        if line.startswith('# '):
            total_lines += 2.0  # H1 headers are taller
        elif line.startswith('## '):
            total_lines += 1.5  # H2 headers
        elif line.strip() == '':
            total_lines += 0.5  # Empty lines
        else:
            # Word wrap: ceil(len / chars_per_line)
            wrapped = max(1, -(-len(line) // chars_per_line))  # Ceiling division
            total_lines += wrapped

    line_height = 24  # ~24px per line in Obsidian
    return base_height + int(total_lines * line_height)
```

**Row alignment:** For nodes in the same horizontal row, calculate all heights first, then use the maximum:
```python
row_texts = ["# Title\n\nShort", "# Title\n\nLonger content\nwith more lines\nand details"]
heights = [estimate_height(t, width=200) for t in row_texts]
row_height = max(heights)  # All nodes in row use this height
```

## Column-Based Flowchart Layout

For flowcharts with parallel columns (like pipelines), use column-based positioning:

```python
# Define columns with fixed x positions and shared width
col_width = 200
col_spacing = 50  # Gap between columns
columns = {
    0: 0,                              # Column 0 starts at x=0
    1: col_width + col_spacing,        # Column 1
    2: 2 * (col_width + col_spacing),  # Column 2
}

# Rows share the same y position across all columns
row_spacing = 30  # Gap between rows
current_y = 0
rows = []

# For each row, calculate height from tallest node, then position all at same y
for row_data in data:
    row_heights = [estimate_height(node['text'], col_width) for node in row_data]
    row_height = max(row_heights)
    rows.append({'y': current_y, 'height': row_height})
    current_y += row_height + row_spacing
```

**Center alignment for straight edges:** To connect nodes with straight vertical lines, align their horizontal centers:
```python
# Node center_x = x + width/2
# For vertical flow, place nodes so centers align vertically
node_x = column_center_x - (node_width / 2)
```

## Straight Connectors

**Vertical flow (top-to-bottom):** Use `fromSide: "bottom"` and `toSide: "top"` for straight vertical arrows:
```json
{
  "fromNode": "step1",
  "fromSide": "bottom",
  "toNode": "step2",
  "toSide": "top"
}
```

**Horizontal flow (left-to-right):** Use `fromSide: "right"` and `toSide: "left"`:
```json
{
  "fromNode": "step1",
  "fromSide": "right",
  "toNode": "step2",
  "toSide": "left"
}
```

**Keep main flow straight:** Align nodes in the primary flow direction so connectors don't bend. Branch connections (secondary flows) can use other sides.

## Python Helper Script

For programmatic canvas generation, use `scripts/create_canvas.py`:

```python
from scripts.create_canvas import CanvasBuilder, estimate_height

canvas = CanvasBuilder()

# Auto-sized nodes (height calculated from content)
n1 = canvas.add_text_node("# Title", x=0, y=0)  # Height auto-calculated
n2 = canvas.add_text_node("Details\nwith multiple\nlines", x=300, y=0)
canvas.add_edge(n1, n2, from_side="right", to_side="left")

# Column-based flowchart
columns = [
    ["# Step 1\n\nDo this first", "# Step 2\n\nThen this"],
    ["# Alt 1\n\nAlternative path", "# Alt 2\n\nAnother option"],
]
canvas.create_column_layout(columns, col_width=200)

canvas.save("output.canvas")
```

Key methods:
- `add_text_node()`, `add_file_node()`, `add_link_node()`, `add_group_node()` - Node creation (height auto-calculated if not specified)
- `add_edge()` - Connect nodes (use `from_side`/`to_side` for straight lines)
- `create_column_layout()` - Column-based flowchart with aligned rows
- `create_grid_layout()`, `create_radial_layout()` - Other layout patterns
- `estimate_height()` - Calculate node height from text content

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
