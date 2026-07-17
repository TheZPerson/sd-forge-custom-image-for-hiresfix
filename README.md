# Hires.Fix Img Swapper
<img width="400"  alt="5685757920120504912544228158420250403177823025122370-2026-07-15-1845439436" src="https://github.com/user-attachments/assets/2436e543-8482-452b-97dd-9490fb7dd971" />

<img width="400"  alt="Preview Image" src="https://github.com/user-attachments/assets/200fe547-9e61-4bda-b1ac-8b905a415aaf" />

This is an Extension for the Forge Webui and related forks. 

This bare bones extension that allows you to change the target image of the Hires Fix.<br>The main use for this is to allow the user to manually fix major problems like extra fingers before upscaling. 

This is meant as quick alternative to fixing flaws by inpainting, generating variations or img2img-tab shenanigans.

You can also add or remove objects before upscaling or just use different image entirely (check Tips).

## Install

Open your WebUIs Extension-Tab. Go to Install from URL tab > Paste this repo's URL into the first field > Click Install

Or 

Manually clone this repo into your extensions folder:

`git clone https://github.com/TheZPerson/sd-forge-custom-image-for-hiresfix`

There is a chance that other extension might overwrite effects of this extension or vice versa.
<br>To mitigate this it is recommend that this extension is run before other extensions that might modify the target image. 

Easiest way to do this is to rename the extension folder to something like: 00-forge-hiresfix-swap. 

## Usage

1. Generate an image.
2. Select image you want to Hires. Fix from the results Gallery, like normal.
3. Export/Copy to image to a photo editor of your choosing and edit flaws out.
<br>(If you are on Neo you can just drag&drop the image directly to the Canvas inside extension and edit image there)
4. Import modified image to the Hires.Fix Img Swapper -extension.
5. While the original image is still selected in the gallery press the Upscale(✨)-button to start the Hires. Fix.
6. The original Hires. Fix image now gets automatically changed to the edited one. 
7. When the Hires. Fix is done, disable the extension   ~or just remove the modified image from the extension.~

## Tips
1. Newer version of Gradio (like in Neo) allows you to paste images directly from the clipboard with CTRL+V.This saves you the hassle of saving image-files to import them. 
2. There is no need to get too detailed with your edits. Hires fix/Adetailer are usually enough to fix any leftovers of your messy edits.
3. It's probably best keep the original and modified image at same dimensions; backend may or may not like the mismatch on sizes. 

## Advanced (follow at your own risk)
I found the default minimum brush weight to be too thick for lineart adjustments. This can be fixed by making following change in the file:

modules_forge/forge_canvas/canvas.js


`ctx.lineWidth = (this.scribbleWidth / (this.scribbleWidthConsistent ? this.imgScale : 1.0)) * 4;`<br>
to<br>
`ctx.lineWidth = (this.scribbleWidth / (this.scribbleWidthConsistent ? this.imgScale : 1.0));`


## Compatibility

Tested to work on fresh installs of __Neo__ and 	__Classic__.
<br>And (not so fresh install of) 	__reForge__

Because how simple the extension is, it might work on other forks as well.
<br>Although I'm not sure if every fork has the Upscale(✨)-button which is fairly essential for the intented workflow. 
