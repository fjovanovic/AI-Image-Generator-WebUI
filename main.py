import sys
from argparse import ArgumentParser
from typing import Union

import gradio as gr
from termcolor import colored

from tabs import TextToImage, ImageToImage


def main(port: Union[int, None], save: bool) -> None:
    with gr.Blocks() as demo:
        with gr.Tab('Text to image'):
            TextToImage(save)
        with gr.Tab('Image to image'):
            ImageToImage(save)

    try:
        demo.launch(
            favicon_path='resources/static/images/logo.png',
            server_port=port
        )
    except OSError as e:
        sys.exit(colored('Port is already active, choose different port', 'red'))


if __name__ == '__main__':
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

    main(args.port, args.save)