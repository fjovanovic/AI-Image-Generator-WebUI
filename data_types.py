from dataclasses import dataclass


@dataclass
class ModelInfo:
    link: str
    info: str


@dataclass
class TextToImageData:
    model: str
    prompt: str
    negative_prompt: str
    scheduler: str
    num_of_images: int
    seed: str
    width: int
    height: int
    inference_steps: int
    cfg_scale: float
    run_on: str