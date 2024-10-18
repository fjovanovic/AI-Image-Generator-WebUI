import sys
from argparse import ArgumentParser
import re

import gradio as gr
from termcolor import colored

from tabs import TextToImage, ImageToImage


def create_demo(save: bool) -> gr.Blocks:
    with gr.Blocks() as demo:
        with gr.Tab('Text to image'):
            TextToImage(save)
        with gr.Tab('Image to image'):
            ImageToImage(save)

    return demo


"""Solving the problem with using 'gradio main.py' to run the app

When saving the changes in the code, the app is being reloaded
and 'demo' variable can't be seen because __name__ can be 
either '__main__' or just 'main' when it's realoaded
so Gradio can't see it
"""
if re.match(r'.*main.*', __name__):
    parser = ArgumentParser(
        usage='python main.py [-p PORT | --port PORT] [-s | --save]',
        description='AI Image Generator WebUI',
        allow_abbrev=False
    )

    parser.add_argument(
        '-p', 
        '--port', 
        type=int, 
        help='Port number for the application'
    )
    parser.add_argument(
        '-s',
        '--save',
        action='store_true',
        help='If included the media and all parameters will be saved on the path ' \
            f'{colored("resources/generated_images/{datetime}/", "dark_grey")}'
    )

    args = parser.parse_args()

    port = args.port
    save = args.save

    demo = create_demo(save)

    try:
        demo.launch(
            favicon_path='resources/static/images/logo.png',
            server_port=port
        )
    except OSError as e:
        sys.exit(colored('Port is already active, choose different port', 'red'))