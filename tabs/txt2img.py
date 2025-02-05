from typing import Union, Dict, Any, List
import sys
import random
import zipfile
import io
import datetime as dt
import os

import gradio as gr
import requests
from PIL import Image

from tabs.tab import Tab
from constants import (
    TXT2IMG_MODELS, 
    TXT2IMG_SCHEDULERS, 
    SAVE_DIR
)
import data_types


class TextToImage(Tab):
    data: data_types.TextToImageData


    def __init__(
        self, 
        save: Union[bool, None],
        base_url: Union[str, None]
    ):
        super().__init__(
            save=save, 
            base_url=base_url,
            endpoint='/txt2img/generate_images'
        )
        self.build_tab()
        self.data = None


    def build_tab(self) -> None:
        model = gr.Dropdown(
            label='Choose pretrained model',
            value='stabilityai/stable-diffusion-xl-base-1.0',
            choices=TXT2IMG_MODELS,
            interactive=True,
            elem_classes='models_dropdown'
        )

        with gr.Row():
            with gr.Column(scale=3):
                prompt = gr.Textbox(
                    label='Prompt', 
                    placeholder='A majestic lion jumping from a big stone at night',
                    lines=2,
                    show_copy_button=True
                )

                negative_prompt = gr.Textbox(
                    label='Negative prompt',
                    placeholder='3D, cartoon, anime, bad anatomy',
                    lines=2,
                    show_copy_button=True
                )
            
            with gr.Column(elem_classes='generate_div'):
                generate_btn = gr.Button(
                    value='Generate',
                    variant='primary',
                    elem_classes='generate_btn'
                )

                save_params_btn = gr.Button(
                    value='Save parameters',
                    variant='secondary',
                    elem_classes='save_params_btn'
                )
        
        with gr.Row():
            with gr.Column():
                scheduler = gr.Radio(
                    choices=TXT2IMG_SCHEDULERS,
                    value='DPM-Solver',
                    label='Scheduler',
                    interactive=True
                )

                num_of_images = gr.Radio(
                    choices=[1, 2, 3, 4],
                    value=4,
                    label='Number of images',
                    interactive=True
                )

                with gr.Row():
                    seed = gr.Number(
                        label='Seed',
                        value=0,
                        scale=9,
                        minimum=0,
                        maximum=sys.maxsize,
                        step=1
                    )

                    seed_btn = gr.Button(
                        variant='stop',
                        value='Generate seed',
                        elem_classes='generate_seed_btn'
                    )

                    seed_btn.click(self.generate_random_seed, outputs=seed)
                
                with gr.Row():
                    width = gr.Slider(
                        label='Width',
                        minimum=512,
                        maximum=1024,
                        interactive=True
                    )

                    height = gr.Slider(
                        label='Height',
                        minimum=512,
                        maximum=1024,
                        interactive=False
                    )

                    width.change(self.changed_width, inputs=width, outputs=height)

                with gr.Row():
                    inference_steps = gr.Slider(
                        label='Inference steps',
                        minimum=10,
                        maximum=50,
                        step=1,
                        value=50,
                        interactive=True
                    )

                    cfg_scale = gr.Slider(
                        label='CFG scale',
                        minimum=1,
                        maximum=10,
                        step=0.1,
                        value=7.5,
                        interactive=True
                    )
                
                with gr.Row():
                    run_on = gr.Radio(
                        choices=['GPU', 'CPU'],
                        value='GPU',
                        label='Run on',
                        interactive=True
                    )
            
            with gr.Column(scale=2):
                gallery = gr.Gallery(
                    label='Generated images',
                    show_label=True,
                    columns=[4],
                    rows=[1],
                    height='auto',
                    preview=True,
                    object_fit='contain',
                    elem_classes='txt2img_generated_images'
                )
        
        generate_btn.click(
            fn=self.disable_btn,
            outputs=generate_btn
        ).then(
            fn=self.generate_text_to_image, 
            inputs=[
                model,
                prompt, 
                negative_prompt,
                scheduler,
                num_of_images,
                seed,
                width,
                height,
                inference_steps,
                cfg_scale,
                run_on
            ], 
            outputs=gallery,
            scroll_to_output=False
        ).then(
            fn=self.enable_btn,
            outputs=generate_btn
        )

        save_params_btn.click(
            fn=self.disable_btn,
            outputs=save_params_btn
        ).then(
            fn=self.save_params
        ).then(
            fn=self.enable_btn,
            outputs=save_params_btn
        )
    

    def generate_random_seed(self) -> int:
        return random.randint(0, sys.maxsize)
    

    def changed_width(self, width: int) -> int:
        return width
    

    def disable_btn(self) -> Dict[str, Any]:
        return gr.update(interactive=False)
    

    def generate_text_to_image(
        self, 
        model: str,
        prompt: str, 
        negative_prompt: str,
        scheduler: str,
        num_of_images: int,
        seed: str,
        width: int,
        height: int,
        inference_steps: int,
        cfg_scale: float,
        run_on: str
    ) -> List[Image.Image]:
        prompt = prompt.strip()
        negative_prompt = negative_prompt.strip()

        if prompt == '':
            raise gr.Error('Prompt field is empty')
        
        params = {
            'model': model,
            'prompt': prompt,
            'negative_prompt': negative_prompt,
            'scheduler': scheduler,
            'num_of_images': num_of_images,
            'seed': seed,
            'width': width,
            'height': height,
            'inference_steps': inference_steps,
            'cfg_scale': cfg_scale,
            'run_on': run_on
        }

        self.data = data_types.TextToImageData(**params)

        url = f'{self.base_url}{self.endpoint}'
        response = requests.get(url, params=params)
        if response.status_code != 200:
            raise gr.Error(f'Failed to fetch images, {response.status_code}')

        images = []
        try:
            zip_data = zipfile.ZipFile(io.BytesIO(response.content))
            if self.save == True:
                current_timestamp = str(dt.datetime.now().replace(microsecond=0)).replace(':', '-')
                dir_path = os.path.join(SAVE_DIR, current_timestamp)
                os.makedirs(dir_path)
                params_str = self.get_params()
                with open(f'{dir_path}/params.txt', 'w') as f:
                    f.write(params_str)
            
            for file_name in zip_data.namelist():
                with zip_data.open(file_name) as file:
                    try:
                        image = Image.open(file).convert('RGB')
                        images.append(image)
                        
                        if self.save == True:
                            image_path = os.path.join(dir_path, file_name)
                            image.save(image_path)
                    except Exception as e:
                        raise gr.Error(f'Error processing {file_name}: {e}')
        except zipfile.BadZipFile:
            raise gr.Error('Failed to extract images: Corrupt zip file')
        
        return images


    def save_params(self) -> None:
        if self.data is None:
            raise gr.Error('Generate image first')
        
        current_timestamp = str(dt.datetime.now().replace(microsecond=0)).replace(':', '-')
        dir_path = os.path.join(SAVE_DIR, current_timestamp)
        os.makedirs(dir_path)
        params_str = self.get_params()
        with open(f'{dir_path}/params.txt', 'w') as f:
            f.write(params_str)
    

    def enable_btn(self) -> Dict[str, Any]:
        return gr.update(interactive=True)
    

    def get_params(self) -> str:
        return '\n'.join(
            f'{key.capitalize().replace("_", " ")}: {value}'
            for (key, value) in self.data.__dict__.items()
        )