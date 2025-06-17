#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from cairosvg import svg2png

def convert_svg_to_png(svg_path, png_path, width=24, height=24):
    """Convert SVG file to PNG"""
    svg2png(url=svg_path, write_to=png_path, output_width=width, output_height=height)

def main():
    """Convert all SVG icons to PNG"""
    icons_dir = os.path.join(os.getcwd(), "icons")
    
    # Get all SVG files
    svg_files = [f for f in os.listdir(icons_dir) if f.endswith(".svg")]
    
    for svg_file in svg_files:
        svg_path = os.path.join(icons_dir, svg_file)
        png_path = os.path.join(icons_dir, svg_file.replace(".svg", ".png"))
        
        print(f"Converting {svg_file} to PNG...")
        convert_svg_to_png(svg_path, png_path, width=48, height=48)
        print(f"Created {png_path}")

if __name__ == "__main__":
    main()