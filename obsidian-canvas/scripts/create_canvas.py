#!/usr/bin/env python3
"""
Obsidian Canvas Creator - Helper script for creating .canvas files
"""

import json
import secrets
import argparse
from typing import List, Dict, Optional, Tuple
import math


class CanvasBuilder:
    """Build Obsidian .canvas files using the JSON Canvas format"""
    
    def __init__(self):
        self.nodes = []
        self.edges = []
        
    def add_text_node(
        self,
        text: str,
        x: int,
        y: int,
        width: int = 250,
        height: int = 200,
        color: Optional[str] = None,
        node_id: Optional[str] = None
    ) -> str:
        """Add a text node with markdown content"""
        node_id = node_id or self._generate_id()
        node = {
            "id": node_id,
            "type": "text",
            "text": text,
            "x": x,
            "y": y,
            "width": width,
            "height": height
        }
        if color:
            node["color"] = color
        self.nodes.append(node)
        return node_id
        
    def add_file_node(
        self,
        file_path: str,
        x: int,
        y: int,
        width: int = 400,
        height: int = 300,
        color: Optional[str] = None,
        subpath: Optional[str] = None,
        node_id: Optional[str] = None
    ) -> str:
        """Add a file reference node"""
        node_id = node_id or self._generate_id()
        node = {
            "id": node_id,
            "type": "file",
            "file": file_path,
            "x": x,
            "y": y,
            "width": width,
            "height": height
        }
        if color:
            node["color"] = color
        if subpath:
            node["subpath"] = subpath if subpath.startswith("#") else f"#{subpath}"
        self.nodes.append(node)
        return node_id
        
    def add_link_node(
        self,
        url: str,
        x: int,
        y: int,
        width: int = 300,
        height: int = 150,
        color: Optional[str] = None,
        node_id: Optional[str] = None
    ) -> str:
        """Add a URL link node"""
        node_id = node_id or self._generate_id()
        node = {
            "id": node_id,
            "type": "link",
            "url": url,
            "x": x,
            "y": y,
            "width": width,
            "height": height
        }
        if color:
            node["color"] = color
        self.nodes.append(node)
        return node_id
        
    def add_group_node(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        label: Optional[str] = None,
        color: Optional[str] = None,
        background: Optional[str] = None,
        background_style: Optional[str] = None,
        node_id: Optional[str] = None
    ) -> str:
        """Add a group container node"""
        node_id = node_id or self._generate_id()
        node = {
            "id": node_id,
            "type": "group",
            "x": x,
            "y": y,
            "width": width,
            "height": height
        }
        if label:
            node["label"] = label
        if color:
            node["color"] = color
        if background:
            node["background"] = background
            if background_style:
                node["backgroundStyle"] = background_style
        # Insert at beginning so groups appear below other nodes
        self.nodes.insert(0, node)
        return node_id
        
    def add_edge(
        self,
        from_node: str,
        to_node: str,
        label: Optional[str] = None,
        from_side: Optional[str] = None,
        to_side: Optional[str] = None,
        from_end: str = "none",
        to_end: str = "arrow",
        color: Optional[str] = None,
        edge_id: Optional[str] = None
    ) -> str:
        """Add an edge connecting two nodes"""
        edge_id = edge_id or self._generate_id()
        edge = {
            "id": edge_id,
            "fromNode": from_node,
            "toNode": to_node
        }
        if label:
            edge["label"] = label
        if from_side:
            edge["fromSide"] = from_side
        if to_side:
            edge["toSide"] = to_side
        if from_end != "none":
            edge["fromEnd"] = from_end
        if to_end != "arrow":
            edge["toEnd"] = to_end
        if color:
            edge["color"] = color
        self.edges.append(edge)
        return edge_id
        
    def create_grid_layout(
        self,
        items: List[str],
        cols: int = 3,
        start_x: int = 0,
        start_y: int = 0,
        spacing_x: int = 500,
        spacing_y: int = 350,
        node_type: str = "text",
        **kwargs
    ) -> List[str]:
        """Create nodes in a grid layout and return their IDs"""
        node_ids = []
        for i, item in enumerate(items):
            row = i // cols
            col = i % cols
            x = start_x + col * spacing_x
            y = start_y + row * spacing_y
            
            if node_type == "text":
                node_id = self.add_text_node(item, x, y, **kwargs)
            elif node_type == "file":
                node_id = self.add_file_node(item, x, y, **kwargs)
            elif node_type == "link":
                node_id = self.add_link_node(item, x, y, **kwargs)
            else:
                raise ValueError(f"Unknown node_type: {node_type}")
            node_ids.append(node_id)
        return node_ids
        
    def create_radial_layout(
        self,
        items: List[str],
        center_x: int = 0,
        center_y: int = 0,
        radius: int = 400,
        start_angle: float = 0,
        node_type: str = "text",
        **kwargs
    ) -> Tuple[List[str], str]:
        """Create nodes in radial layout around a center node. Returns (node_ids, center_id)"""
        # Create center node
        center_id = self.add_text_node(
            "Center",
            center_x - 125,
            center_y - 100,
            width=250,
            height=200,
            **kwargs
        )
        
        node_ids = []
        for i, item in enumerate(items):
            angle = start_angle + (2 * math.pi * i) / len(items)
            x = int(center_x + radius * math.cos(angle)) - 125
            y = int(center_y + radius * math.sin(angle)) - 100
            
            if node_type == "text":
                node_id = self.add_text_node(item, x, y, **kwargs)
            elif node_type == "file":
                node_id = self.add_file_node(item, x, y, **kwargs)
            elif node_type == "link":
                node_id = self.add_link_node(item, x, y, **kwargs)
            else:
                raise ValueError(f"Unknown node_type: {node_type}")
            node_ids.append(node_id)
            
            # Connect to center
            self.add_edge(center_id, node_id)
            
        return node_ids, center_id
        
    def to_json(self, indent: int = 2) -> str:
        """Export canvas as JSON string"""
        canvas = {}
        if self.nodes:
            canvas["nodes"] = self.nodes
        if self.edges:
            canvas["edges"] = self.edges
        return json.dumps(canvas, indent=indent)
        
    def save(self, filepath: str):
        """Save canvas to .canvas file"""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(self.to_json())
            
    @staticmethod
    def _generate_id() -> str:
        """Generate unique node/edge ID (16-char hex like Obsidian)"""
        return secrets.token_hex(8)


def create_example_mindmap(output_path: str):
    """Create an example mind map canvas"""
    canvas = CanvasBuilder()
    
    # Create central node
    center_id = canvas.add_text_node(
        "**Main Topic**\n\nCentral concept",
        x=0,
        y=0,
        width=300,
        height=200,
        color="1"
    )
    
    # Create branch nodes
    branches = [
        ("Subtopic 1\n\nDetails here", 500, -200, "2"),
        ("Subtopic 2\n\nMore info", 500, 100, "3"),
        ("Subtopic 3\n\nAdditional points", -500, -200, "4"),
        ("Subtopic 4\n\nExtra details", -500, 100, "5"),
    ]
    
    for text, x, y, color in branches:
        node_id = canvas.add_text_node(text, x, y, color=color)
        canvas.add_edge(center_id, node_id)
    
    canvas.save(output_path)
    print(f"Created mind map at: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Create Obsidian .canvas files"
    )
    parser.add_argument(
        "--output",
        "-o",
        default="output.canvas",
        help="Output .canvas file path"
    )
    parser.add_argument(
        "--example",
        choices=["mindmap"],
        help="Create example canvas"
    )
    
    args = parser.parse_args()
    
    if args.example == "mindmap":
        create_example_mindmap(args.output)
    else:
        # Create empty canvas
        canvas = CanvasBuilder()
        canvas.save(args.output)
        print(f"Created empty canvas at: {args.output}")


if __name__ == "__main__":
    main()
