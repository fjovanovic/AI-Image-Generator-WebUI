from typing import Union
import numpy as np
import random
import sys

import gradio as gr

from tabs.tab import Tab
from constants import *


class ImageToImage(Tab):
    def __init__(
        self, 
        save: Union[bool, None],
        base_url: Union[str, None]
    ):
        super().__init__(
            save=save, 
            base_url=base_url,
            endpoint='/img2img/generate_images'
        )
        self.build_tab()
    

    def build_tab(self) -> None:
        model = gr.Dropdown(
            label='Choose pretrained model',
            value='stabilityai/sdxl-turbo',
            choices=TXT2IMG_MODELS,
            interactive=True,
            elem_classes='models_dropdown'
        ) 

        with gr.Row():
            prompt = gr.Textbox(
                label='Prompt', 
                placeholder='Pikachu fine dining with a view to the Eiffel Tower ',
                lines=2,
                show_copy_button=True
            )

            negative_prompt = gr.Textbox(
                label='Negative prompt',
                placeholder='3D, cartoon, anime, bad anatomy',
                lines=2,
                show_copy_button=True
            )

        with gr.Row(elem_classes='img2img_images_div'):
            input_image = gr.Image(
                elem_classes='img2img_image'
            )

            generate_btn = gr.Button(
                value='Generate',
                variant='primary',
                elem_classes='img2img_generate_btn'
            )

            output_image = gr.Image(
                elem_classes='img2img_image'
            )

        generate_btn.click(
            self.generate_image_to_image, 
            inputs=[
                model,
                prompt,
                negative_prompt,
                input_image
            ], 
            outputs=output_image
        )


    def generate_random_seed(self) -> int:
        return random.randint(0, sys.maxsize)


    def changed_width(self, width: int) -> int:
        return width


    def generate_image_to_image(
        self,
        model: str,
        prompt: str,
        negative_prompt: str,
        input_image: np.ndarray
    ):
        ...