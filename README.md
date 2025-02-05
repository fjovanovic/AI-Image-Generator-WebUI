# AI Image Generator WebUI 
This project is a web-based AI image generator powered by [Stable Diffusion](https://github.com/Stability-AI/stablediffusion) and [Gradio](https://www.gradio.app/). 
It provides an intuitive interface accessible through a web browser, allowing users to generate images using both text-to-image and image-to-image models. 
With its user-friendly design, the WebUI makes AI-powered image creation simple and efficient.  
Even if you don't have powerful hardware, you can run backend using Google Colab.  
The backend for this project is available on [this repository](https://github.com/fjovanovic/Stable-Diffusion-WebUI-Backend), providing the full code and setup instructions 

## Examples 
- Example of **Text to image** generation
  
  <img src="/resources/examples/txt2img.png" alt="Text to image" height=600>
- Example of **Image to image** generation
  
  <img src="/resources/examples/img2img.png" alt="Text to image" height=600>

## Prerequisites 
- ![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg) 
- `venv`
  
  > Before installing dependencies it is highly recommended to work in [virtual environment](https://docs.python.org/3/library/venv.html).
  > If you want to create virtual environment `.venv`, use following command:
  > ```bash
  >  python -m venv .venv
  >  ```
  > Make sure it is activated after installation

- `backend`

  > Clone [backend](https://github.com/fjovanovic/Stable-Diffusion-WebUI-Backend)  
  > Start the FastAPI backend using instructions from that repository

## Install dependencies
```bash
pip install -r requirements.txt
```

## Arguments 
- Use `python main.py --help`
- `[-p PORT | --port PORT]`

  > Port on local host that will serve the app

- `[-s | --save]`

  > If included, generated images including all parameters used to generate images will be saved on the path **resources/generated_images/{datetime}/**

- `[--base-url BASE_URL]`

  > Url for the backend API, if not included then it will be hosted on the localhost
