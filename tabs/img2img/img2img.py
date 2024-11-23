from typing import Union, Dict, Any
import random
import sys
import io

import gradio as gr
import numpy as np
from PIL import Image
import requests

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
            endpoint='/img2img/generate_image'
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
                placeholder='Pikachu fine dining with a view to the Eiffel Tower',
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
            self.disable_btn,
            outputs=generate_btn
        ).then(
            self.generate_image_to_image, 
            inputs=[
                model,
                prompt,
                negative_prompt,
                input_image
            ], 
            outputs=output_image
        ).then(
            self.enable_btn,
            outputs=generate_btn
        )


    def generate_random_seed(self) -> int:
        return random.randint(0, sys.maxsize)


    def changed_width(self, width: int) -> int:
        return width


    def disable_btn(self) -> Dict[str, Any]:
        return gr.update(interactive=False)


    def generate_image_to_image(
        self,
        model: str,
        prompt: str,
        negative_prompt: str,
        input_image: np.ndarray
    ) -> Image:
        prompt = prompt.strip()
        negative_prompt = negative_prompt.strip()

        if input_image is None:
            raise gr.Error('Upload input image')
        
        if prompt == '':
            raise gr.Error('Prompt field is empty')
        
        img = Image.fromarray(input_image)
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)

        payload = {
            'model': model,
            'prompt': prompt,
            'negative_prompt': negative_prompt
        }

        files = {
            'file': (
                'image.png', 
                buffer, 
                'image/png'
            )
        }

        url = f'{self.base_url}{self.endpoint}'
        response = requests.post(url, data=payload, files=files)
        if response.status_code != 200:
            raise gr.Error(f'Problem with response, status code: {response.status_code}')

        return Image.open(io.BytesIO(response.content))


    def enable_btn(self) -> Dict[str, Any]:
        return gr.update(interactive=True)