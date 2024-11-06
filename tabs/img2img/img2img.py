import gradio as gr
from typing import Union

from ..tab import Tab


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
        gr.Markdown('TODO')