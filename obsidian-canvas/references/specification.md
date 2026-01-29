# JSON Canvas Specification Reference

Complete specification for the JSON Canvas format (v1.0).

## Top-Level Structure

```json
{
  "nodes": [],  // optional array
  "edges": []   // optional array
}
```

## Node Types

### Common Node Attributes

All nodes must include:
- `id` (string, required) - Unique identifier
- `type` (string, required) - "text", "file", "link", or "group"
- `x` (integer, required) - X position in pixels
- `y` (integer, required) - Y position in pixels
- `width` (integer, required) - Width in pixels
- `height` (integer, required) - Height in pixels

Optional for all nodes:
- `color` (canvasColor) - See color section

### Text Node

Stores text content with Markdown support.

**Additional attributes:**
- `text` (string, required) - Plain text with Markdown syntax

**Example:**
```json
{
  "id": "abc123",
  "type": "text",
  "text": "# Heading\n\n**Bold** text",
  "x": 0,
  "y": 0,
  "width": 250,
  "height": 200,
  "color": "1"
}
```

### File Node

References files or attachments within the vault.

**Additional attributes:**
- `file` (string, required) - Path to file within system
- `subpath` (string, optional) - Link to heading/block, starts with `#`

**Example:**
```json
{
  "id": "def456",
  "type": "file",
  "file": "Notes/Meeting.md",
  "subpath": "#Action Items",
  "x": 300,
  "y": 0,
  "width": 400,
  "height": 300
}
```

### Link Node

References external URLs.

**Additional attributes:**
- `url` (string, required) - The URL

**Example:**
```json
{
  "id": "ghi789",
  "type": "link",
  "url": "https://example.com",
  "x": 0,
  "y": 250,
  "width": 300,
  "height": 150,
  "color": "#3498db"
}
```

### Group Node

Visual container for organizing other nodes.

**Additional attributes:**
- `label` (string, optional) - Text label for the group
- `background` (string, optional) - Path to background image
- `backgroundStyle` (string, optional) - Rendering style for background
  - `"cover"` - Fills entire width and height
  - `"ratio"` - Maintains aspect ratio
  - `"repeat"` - Repeats as pattern

**Example:**
```json
{
  "id": "jkl012",
  "type": "group",
  "label": "Category A",
  "x": -50,
  "y": -50,
  "width": 800,
  "height": 600,
  "color": "2"
}
```

## Edges

Edges connect nodes with directional lines.

**Required attributes:**
- `id` (string, required) - Unique identifier
- `fromNode` (string, required) - Source node ID
- `toNode` (string, required) - Target node ID

**Optional attributes:**
- `fromSide` (string) - Connection side on source node
  - Valid: "top", "right", "bottom", "left"
- `toSide` (string) - Connection side on target node
  - Valid: "top", "right", "bottom", "left"
- `fromEnd` (string) - Endpoint shape at start (default: "none")
  - Valid: "none", "arrow"
- `toEnd` (string) - Endpoint shape at end (default: "arrow")
  - Valid: "none", "arrow"
- `color` (canvasColor) - Line color
- `label` (string) - Text label for edge

**Example:**
```json
{
  "id": "edge-1",
  "fromNode": "abc123",
  "toNode": "def456",
  "fromSide": "right",
  "toSide": "left",
  "label": "leads to",
  "color": "4"
}
```

## Colors (canvasColor)

Colors can be specified as:

### Preset Colors

Six preset colors mapped to numbers:
- `"1"` - Red
- `"2"` - Orange
- `"3"` - Yellow
- `"4"` - Green
- `"5"` - Cyan
- `"6"` - Purple

**Note:** Exact color values intentionally undefined so applications can customize to their brand/theme.

### Hex Colors

Standard hex format: `"#RRGGBB"`

Examples:
- `"#FF0000"` - Red
- `"#00FF00"` - Green
- `"#0000FF"` - Blue
- `"#3498db"` - Light blue

## Z-Index Ordering

Nodes appear in the order they're listed in the array:
- **First node** = bottom layer (appears behind others)
- **Last node** = top layer (appears in front)

Best practice: Place group nodes first, then contained nodes.

## File Paths

For `file` nodes and group `background` attributes:
- Use forward slashes `/` for path separators
- Paths are relative to vault root
- Can reference any file type (images, PDFs, other notes, etc.)

Examples:
- `"Notes/Meeting.md"`
- `"Assets/diagram.png"`
- `"Projects/2024/Q1/report.pdf"`

## Validation Checklist

Before saving a .canvas file:

1. ✓ Valid JSON syntax
2. ✓ All node IDs are unique
3. ✓ All edge `fromNode`/`toNode` reference existing node IDs
4. ✓ All required attributes present
5. ✓ Node `type` values are valid ("text", "file", "link", "group")
6. ✓ Edge endpoint values valid ("none", "arrow")
7. ✓ Edge side values valid ("top", "right", "bottom", "left")
8. ✓ Color values use correct format (preset "1"-"6" or hex "#RRGGBB")
9. ✓ Subpath starts with `#` if present
10. ✓ File paths exist (if referencing vault files)

## Minimal Valid Canvas

The simplest valid .canvas file:

```json
{}
```

Single text node:

```json
{
  "nodes": [
    {
      "id": "1",
      "type": "text",
      "text": "Hello",
      "x": 0,
      "y": 0,
      "width": 250,
      "height": 200
    }
  ]
}
```

## Canvas with Everything

Example showcasing all features:

```json
{
  "nodes": [
    {
      "id": "group-1",
      "type": "group",
      "label": "Container",
      "x": -100,
      "y": -100,
      "width": 900,
      "height": 700,
      "color": "1",
      "background": "Assets/bg.png",
      "backgroundStyle": "cover"
    },
    {
      "id": "text-1",
      "type": "text",
      "text": "# Title\n\nContent",
      "x": 0,
      "y": 0,
      "width": 250,
      "height": 200,
      "color": "2"
    },
    {
      "id": "file-1",
      "type": "file",
      "file": "Notes/doc.md",
      "subpath": "#Section",
      "x": 300,
      "y": 0,
      "width": 400,
      "height": 300,
      "color": "3"
    },
    {
      "id": "link-1",
      "type": "link",
      "url": "https://example.com",
      "x": 0,
      "y": 250,
      "width": 300,
      "height": 150,
      "color": "#FF5733"
    }
  ],
  "edges": [
    {
      "id": "edge-1",
      "fromNode": "text-1",
      "toNode": "file-1",
      "fromSide": "right",
      "toSide": "left",
      "fromEnd": "none",
      "toEnd": "arrow",
      "label": "references",
      "color": "4"
    },
    {
      "id": "edge-2",
      "fromNode": "file-1",
      "toNode": "link-1",
      "label": "see also"
    }
  ]
}
```
