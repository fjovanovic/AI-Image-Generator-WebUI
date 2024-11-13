import os
from pathlib import Path
from typing import Dict
import json

import data_types


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


def load_models_info(path: str) -> Dict[str, data_types.ModelInfo]:
    with open(path, 'r') as f:
        models_json: dict = json.load(f)
    
    return {
        name: data_types.ModelInfo(**info) 
        for (name, info) in models_json.items()
    }