import os
from pathlib import Path


def get_css(root: str) -> str:
    css_files = []
    for file in os.listdir(root):
        path = Path(root) / file
        css_files.append(path.as_posix())
    
    css = ''
    for file in css_files:
        with open(file, 'r') as f:
            css += f.read()
            css += '\n'
    
    return css