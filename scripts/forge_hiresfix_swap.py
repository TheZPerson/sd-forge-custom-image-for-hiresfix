import gradio as gr
from torchvision.transforms.functional import _is_pil_image
from modules import scripts
from modules.processing import StableDiffusionProcessing
from modules.ui_components import InputAccordion

import numpy as np

try:
    from modules_forge.forge_canvas.canvas import ForgeCanvas
except ImportError:
    is_neo = False
else:
    is_neo = True

class Forge_HiresFix_Swap(scripts.Script):

    def __init__(self):
        super().__init__()

    def title(self):
        return "Hires Fix Img Swapper"

    def ui(self, is_img2img):
          with InputAccordion(False, label=self.title()) as enable:
            if is_neo:
                inputImage = ForgeCanvas(scribble_color="#FFFFFF", scribble_softness=25)
                inputImage.do_not_save_to_config = True
            else:
                inputImage = gr.Image(type="pil",label="img",show_label=False)

            if is_neo:
                return [enable, inputImage.background ,inputImage.foreground]
            else:
                return [enable, inputImage, inputImage]

    def show(self, is_img2img: bool):
          return scripts.AlwaysVisible if is_img2img is False else False

    def process(self, p: StableDiffusionProcessing, enable,inputImageBG, inputImageFG):

        if p.firstpass_image is None or hasattr(p, "_ad_inner") or inputImageBG is None or _is_pil_image(inputImageBG) is False or enable is False:
            return

        outputImage = inputImageBG
         
        if is_neo and _is_pil_image(inputImageFG) is True:
            outputImage = Forge_HiresFix_Swap.merge(np.array(inputImageBG),np.array(inputImageFG))


        p.firstpass_image = outputImage
     

    def merge(bg: np.ndarray, fg: np.ndarray):
        if fg is None:  # first stroke
            return bg
        bg_rgb = bg[..., :3].astype(np.float32)
        fg_rgb = fg[..., :3].astype(np.float32)
        alpha = fg[..., 3:4].astype(np.float32) / 255.0
        merged = fg_rgb * alpha + bg_rgb * (1.0 - alpha)

        return np.clip(merged.round(), 0, 255).astype(np.uint8)
