import sys
import random
from typing import Union

import gradio as gr

from ..tab import Tab
from constants import TXT2IMG_MODELS, TXT2IMG_SCHEDULERS


class TextToImage(Tab):
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


    def build_tab(self) -> None:
        gr.Dropdown(
            label='Choose pretrained model',
            value='CompVis/stable-diffusion-v1-1',
            choices=TXT2IMG_MODELS,
            interactive=True,
            elem_classes='models_dropdown'
        )

        with gr.Row():
            with gr.Column(scale=3):
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
                    seed = gr.Textbox(
                        label='Seed',
                        scale=9,
                        show_copy_button=True
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
                        maximum=1024
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
            
            with gr.Column(scale=2):
                gallery = gr.Gallery(
                    label='Generated images',
                    show_label=True,
                    columns=[4],
                    rows=[1],
                    height='auto',
                    preview=True,
                    object_fit='contain'
                )
        
        generate_btn.click(
            fn=self.disable_generate_btn,
            outputs=[generate_btn]
        ).then(
            fn=self.generate_text_to_image, 
            inputs=[
                prompt, 
                negative_prompt,
                scheduler,
                num_of_images,
                seed,
                width,
                height,
                inference_steps,
                cfg_scale
            ], 
            outputs=[
                gallery, 
                generate_btn
            ]
        )
    

    def generate_random_seed(self) -> int:
        return random.randint(0, sys.maxsize)
    

    def changed_width(self, width: int) -> int:
        return width
    

    def disable_generate_btn(self):
        return gr.update(interactive=False)
    

    def generate_text_to_image(
        self, 
        prompt: str, 
        negative_prompt: str,
        scheduler: str,
        num_of_images: int,
        seed: str,
        width: int,
        height: int,
        inference_steps: int,
        cfg_scale: float
    ) -> str:
        ...