import sys
from argparse import ArgumentParser
import re
from typing import Union

import gradio as gr
from termcolor import colored

from tabs import TextToImage, ImageToImage
import utils


def create_demo(
    save: Union[bool, None], 
    base_url: Union[str, None]
) -> gr.Blocks:
    css = utils.get_css('resources/static/css')

    with gr.Blocks(css=css) as demo:
        with gr.Tab('Text to image'):
            TextToImage(save, base_url)
        with gr.Tab('Image to image'):
            ImageToImage(save, base_url)

    return demo


"""Solving the problem with using 'gradio main.py' to run the app

When saving the changes in the code, the app is being reloaded
and 'demo' variable can't be seen because __name__ can be 
either '__main__' or just 'main' when it's realoaded
so Gradio can't see it
"""
if re.match(r'.*main.*', __name__):
    parser = ArgumentParser(
        usage='python main.py [-p PORT | --port PORT] [-s | --save] '\
            '[--api-url API_URL]',
        description='AI Image Generator WebUI',
        allow_abbrev=False
    )

    parser.add_argument(
        '-p', 
        '--port', 
        type=int, 
        help='port number for the application'
    )
    parser.add_argument(
        '-s',
        '--save',
        action='store_true',
        help='if included the media and all parameters will be saved on the path ' \
            f'{colored("resources/generated_images/{datetime}/", "dark_grey")}'
    )
    parser.add_argument(
        '--base-url',
        action='store',
        help='base API url for the backend',
        dest='base_url'
    )

    args = parser.parse_args()
    demo = create_demo(args.save, args.base_url)

    try:
        demo.launch(
            favicon_path='resources/static/images/logo.png',
            server_port=args.port
        )
    except OSError as e:
        sys.exit(colored('Port is already active, choose different port', 'red'))