from typing import Tuple, Dict, Any

import gradio as gr

import utils
import data_types


class Models:
    models: Dict[str, data_types.ModelInfo]
    default_model: str


    def __init__(self):
        self.models = utils.load_models_info('resources/static/data/models.json')
        self.default_model = 'stabilityai/stable-diffusion-xl-base-1.0'
        self.build_tab()
    

    def build_tab(self) -> None:
        model = gr.Dropdown(
            label='Choose pretrained model',
            value=self.default_model,
            choices=self.models.keys(),
            interactive=True,
            elem_classes='models_dropdown'
        )

        link_btn = gr.Button(
            value='Link',
            icon='resources/static/images/link_button.png',
            link=self.models[self.default_model].link,
            variant='primary',
            elem_classes='models_link'
        )

        info = gr.Markdown(
            value=self.models[self.default_model].info,
            elem_classes='model_info'
        )

        model.change(self.model_chosen, inputs=model, outputs=[link_btn, info])
    

    def model_chosen(self, model: str) -> Tuple[Dict[str, Any], str]:
        return (
            gr.update(link=self.models[model].link),
            self.models[model].info
        )