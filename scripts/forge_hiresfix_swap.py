import gradio as gr
from torchvision.transforms.functional import _is_pil_image
from modules import scripts, shared, script_callbacks
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

    sorting_priority =getattr(shared.opts, "hires_fix_sortOrder",-995)

    def __init__(self):
        super().__init__()

    def title(self):
        return "Hires Fix Img Swapper"

    def ui(self, is_img2img):
          with InputAccordion(False, label=self.title()) as enable:
            if is_neo:
                inputImage = ForgeCanvas(height = getattr(shared.opts, "hires_fix_swap_maxheight",300), scribble_color=getattr(shared.opts, "hires_fix_swap_color","#ffffff"), scribble_softness=getattr(shared.opts, "hires_fix_swap_canvasSoftness",100), scribble_width=getattr(shared.opts, "hires_fix_swap_size",25), scribble_alpha=getattr(shared.opts, "hires_fix_swap_opacity",100)  )
                inputImage.do_not_save_to_config = True
            else:
                inputImage = gr.Image(height = getattr(shared.opts, "hires_fix_swap_maxheight",300),type="pil",label="img",show_label=False)

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


def on_ui_settings():
    section = ("hires_fix_swap", "Hires Fix Img Swapper")
    shared.opts.add_option("hires_fix_swap_maxheight",shared.OptionInfo(default=300,label="Canvas Max Height", component=gr.Number, component_args = {'precision':0, 'minimum': 0,},section=section).needs_reload_ui())
    shared.opts.add_option("hires_fix_sortOrder",shared.OptionInfo(default=-995,label="Extension Sort Order", component=gr.Number, component_args = {'precision':0},section=section).needs_reload_ui())

    if is_neo:
        shared.opts.add_option("hires_fix_swap_canvasSoftness",shared.OptionInfo(default=25,label="Brush Softness", component=gr.Number, component_args = {'precision':0, 'minimum': 0, 'maximum' : 100 },section=section).needs_reload_ui())
        shared.opts.add_option("hires_fix_swap_size",shared.OptionInfo(default=100,label="Brush Size", component=gr.Number, component_args = {'precision':0, 'minimum': 1, 'maximum' : 100 },section=section).needs_reload_ui())
        shared.opts.add_option("hires_fix_swap_color",shared.OptionInfo(default="#ffffff",label="Brush Color",component=gr.ColorPicker,section=section).needs_reload_ui())
        shared.opts.add_option("hires_fix_swap_opacity",shared.OptionInfo(default=100,label="Brush Opacity", component=gr.Number, component_args = {'precision':0, 'minimum': 0, 'maximum' : 100 },section=section).needs_reload_ui())

script_callbacks.on_ui_settings(on_ui_settings)