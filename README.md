# Primere nodes for ComfyUI

Git link: https://github.com/CosmicLaca/ComfyUI_Primere_Nodes

<a href="./Workflow/readme_images/latest_workflow.png" target="_blank"><img src="./Workflow/readme_images/latest_workflow.jpg" width="400px"></a>
<hr>

## Special features in attached most complex workflow **Primere_latest_workflow.json**:
- Automatically detect if SD or SDXL checkpoint loaded, and control the whole process (e.g. resolution) by the result
- No need to set/switch nodes or workflow between SD and SDXL checkpoints
- You can select prefered model, subpath and orientation under the prompt input to overwrite the system settings by prompt node, same settings under the .csv prompt loader node
- You can randomize the image orientation if using batch mode
- One button LCM and Turbo mode (see example workflow), the LCM mode download required SD and SDXL LCM models at first usage
- Save image and .json and/or .txt file with workflow details, but these details saved to image as EXIF too
- Read original A1111 styles.csv file, handle dynamic prompts and additional networks from the text content of prompts like in A1111, example dynamic styles.csv included
- Not just .csv usefil as prompt source, organize your prompts to .toml file, and use the file content on dedicated prompt organizer node
- Random noise generator for latent image, with special function to generate different but consistent images with locked seed with adjustable difference between min and max values 
- Additional and easy editable image styles included in the text encoder as list
- Resolution selector by side ratios only, editable ratio source in external file, auto detect checkpoint version for right final size
- Image size can be convert to "standard" (x16) values, fully customizable side ratios by float numbers at the bottom of the resolution selector node
- Original image size multiplied to upscaler by three several ratios, one for SD and another one for SDXL models and third for Turbo checkpoints
- Not just multiply original resolution by integer as multiplier, but can be define the final resolution by megapixels ffrom any image sizes
- Image size multiplier can solve low memory error problem if using Ultimate SD Upscaler 
- Remove previously included networks from the content of prompts (Embedding, Lora, Lycoris and Hypernetwork), use it if the used model incompatible with them, or if you want to try your prompt without included networks or want to change to different networks, or using SDXL checkpoint and SD Loras have to be changed to SDXL compatible version 
- Embedding handler for A1111 compatible prompts (or .csv styles), this node convert A1111 Embeddings to ComfyUI
- Use more than one prompt or style inputs for testing, comparison and developing new prompts, and select any by 'Prompt Switch' node
- Special image META/EXIF reader, which handle model name and samplers from A1111/ComfyUI .png or .jpg, never was easier to recycle your older A1111 or ComfyUI images and re-using them with same or different settings. With switches you can change or keep the original embedd seed/model/size/etc... to workflow settings
- Realtime check/debug generation details by nodes as text
- Workflow and nodes support Lycoris in dedicated node, no need to copy them to Loras path
- Adjustable detailers and refiners for face, eye, hands, mouth, fashion wear, etc..., separated prompt input for detailers can be mixed to original for better result
- Detailers automatically detect and support LCM and Turbo concepts
- Visual (select element by preview image) loaders available for Checkpoints, Loras, Lycoris, Embedding, Hypernetworks, and saved Styles. You only have to create preview images to right name and path
- Midjourney art-style prompts can be attached to the original prompt
- Emotions as style

<hr>

## Do it before first run, or the example workflow / nodes will be failed in your local environment:

**Try load 'Primere_latest_workflow.json' from the 'Workflow' folder, specially after git pull if the previous workflow failed because nodes changed by develpment. This node contains most of developed nodes, but 3rd party nodes and models required**

1; Install missing Python libraries if not start for first try. **Activate Comfy venv** and use 'pip install -r requirements.txt' at the root folder of Primere nodes (or check error messages and install missing libs manually).

2; If nodepack started, use the Primere_latest_workflow or Primere_basic_workflow on the 'Workflow' folder for first try. All separated nodes visible under the 'Primere Nodes' submenu if you need nodes for custom workflow. If some other nodes missing and red in workflow, download or delete unloaded 3rd party nodes.

3; The **Primere_latest_workflow.json** is the most complex workflow, using most of developed nodes. But the **Primere_basic_workflow.json** is simple basic workflow with less required nodes. If the complex latest workflow not start or failed, please test out the basic or the minimal instead. If you save own workflow with older developed nodes, try 'Fix node (recreate)' menu on right-click after git pull. 

4; Set the right path for image saving in the node 'Primere Image Meta Saver' on 'output_path' input.

5; Rename 'styles.example.csv' on the 'stylecsv' folder to 'syles.csv' or copy here your own A1111 .csv file if you want to use your custom 'Primere Styles' node. If you keep or rename the original 'styles.example.csv', you will see image previews for example prompts included.

6; **Set existing values for all combos from your own environment.** Checkpoint, Lora, Lycoris, Style, Embedding, Upscale model, Detailer models, Primere Image Meta Saver and Hypernetwork selectors will be failed if not change right values on all input fields from your own environment.

7; Choose your own image from your machine to the 'Primere Exif Reader'.

8; **Update your Comfy to latest version** if workflow failed. I always do it before development, so my nodes and the workflow compatible with latest Comfy version.

9; I develop my nodes and workflow continously, so do git pull from master branch once a week, and refresh nodes in saved custom workflow if required. **'Fix node (recreate)'** menu will keep previous connections.

10; Sometime the node development change existing nodes, so the previous workflow failed after pull, usually with invalid input value. Then use right-click + **'Fix node (recreate)' menu** and maybe need to rewire changed nodes, or load the attached example workflows again if updated.

11; Remove dynamic prompts from the filled prompt input nodes I used before the example workflow saved and pushed. Maybe you have missing wildcard files (https://civitai.com/tag/wildcard), and sometime the wildcard decoder sending error if source file not found. If you have wildcard files, just copy them to the 'wildcards' folder.

12; Don't overwrite attached example workflows, because the git pull will write back to the original. Ff you modify, save as them to another name and path. 

<hr>

<a href="./Workflow/readme_details/WFComparison.md" target="_blank"><img src="./Workflow/readme_images/WFComparison.png" height="150px"></a>

<hr>

# Nodes in the pack grouped by submenus:

## Submenu :: Visuals:

### Before you save your own previews, just set 'show_modal' input to 'false'

Here are same functions similar like in **Inputs** submenu, but the selection (for example checkpoints, loras, lycoris, embeddings, styles from style.csv and hypernetworks) **possible by image previews on modal**. Very similar than in several themes of A1111, but you must create previews to right path.
You have to create and save images as previews to the right path and name, deails later. Previews can be **only .jpg** format with .jpg extension. 
Don't use large files because the modal loading time. The preview height in visual selector modal is only 220px, so don't use upscaled or original images as preview. Downsize your previews height to 250-300 px, and set jpg image quality to ~50% for faster loading. ACDSee do it automatically at Tools->Batch->Resize menu if you already have large images, if you generate new, just set the upscaler under the 1 (0.4 for SD and 0.2 for SDXL is good enought, while set the jpeg quality to ~50-60 in the image saver node).
Checkpoint and additional networks files have a badge with SD or SDXL version. The version info is cached, so only one time needed to read and store. When you use your checkpoint or networks first time, the version info will be saved to the 'Nodes\.cache\.cache.json' file, next time just read back from cached json. About automatic mass version caching read more later.

**If you need version info of all your files for visual modal badges, you can use helper files from the 'terminal_helpers' subdir:**
- Open terminal/command window, and activate your comfy venv. This is the most important step before run command line helpers.
- In the terminal window you already activated your venv, just run included .py files:
- **lora_version_cache.py** will be read and store versions of all lora files
- **lyco_version_cache.py** will be read and store versions of all lycoris files
- **model_version_cache.py** will be read and store versions of all checkpoint files
- **embedding_version_cache.py** will be read and store versions of all textual embedding files

Unfortunately the result is not perfect :(. You must check the version labels on your models and network files. If failed or unknown, you can modify and correct the .cache.json manually. Git pull will keep your edited cache file.
**The embedding cache helper can't read the right version of embedding files**, so after first run all files will be marked as **SD** version. You must modify and replace SD to SDXL in the .cache.json manually.

<hr>
Example of visual checkpoint selector if preview available:

<a href="./Workflow/readme_images/pvisualmodal.jpg" target="_blank"><img src="./Workflow/readme_images/pvisualmodal.jpg" height="300px"></a>
<hr>

### Primere Visual CKPT selector:
**Visual selector for checkpoints**. You must mirror your original checkpoint subdirs **(not the checkpoint files!)** to ComfyUI\custom_nodes\ComfyUI_Primere_Nodes\front_end\images\checkpoints\ path but only the preview images needed, same name as the checkpoint but with .jpg only extension.
As extra features you can enable/disable modal with 'show_modal' switch, and exclude files and paths from modal starts with . (point) character if show_hidden switch is off.

<a href="./Workflow/readme_images/pvmodal.jpg" target="_blank"><img src="./Workflow/readme_images/pvmodal.jpg" height="120px"></a>
<hr>

### Primere Visual Lora selector:
Same as than the 'Primere LORA' node, but with preview images of selection modal.  
You must mirror your original lora subdirs **(not your lora files!)** to ComfyUI\custom_nodes\ComfyUI_Primere_Nodes\front_end\images\loras\ path but only the preview images needed, same name as the lora files but with .jpg only extension.
As extra features you can enable/disable modal with 'show_modal' switch, and exclude files and paths from modal starts with . (point) character if show_hidden switch is off.

<a href="./Workflow/readme_images/pvlora.jpg" target="_blank"><img src="./Workflow/readme_images/pvlora.jpg" height="300px"></a>
<hr>

### Primere Visual Lycoris selector:
Same as than the 'Primere LYCORIS' node, but with preview images of selection modal.  
You must mirror your original lycoris subdirs **(not your lycoris files!)** to ComfyUI\custom_nodes\ComfyUI_Primere_Nodes\front_end\images\lycoris\ path but only the preview images needed, same name as the lyco files but with .jpg only extension.
As extra features you can enable/disable modal with 'show_modal' switch, and exclude files and paths from modal starts with . (point) character if show_hidden switch is off.

<a href="./Workflow/readme_images/pvlyco.jpg" target="_blank"><img src="./Workflow/readme_images/pvlyco.jpg" height="200px"></a>
<hr>

### Primere Visual Embedding selector:
Same as than the 'Primere Embedding' node, but with preview images of selection modal.  
You must copy your original embedding subdirs **(not your embedding files!)** to ComfyUI\custom_nodes\ComfyUI_Primere_Nodes\front_end\images\embeddings\ path but only the preview images needed, same name as the embedding file but with .jpg only extension.
As extra features you can enable/disable modal with 'show_modal' switch, and exclude files and paths from modal starts with . (point) character if show_hidden switch is off.

<a href="./Workflow/readme_images/pvembedd.jpg" target="_blank"><img src="./Workflow/readme_images/pvembedd.jpg" height="300px"></a>
<hr>

### Primere Visual Hypernetwork selector:
Same as than the 'Primere Hypernetwork' node, but with preview images of selection modal.  
You must copy your original hypernetwork subdirs **(not your hypernetwork files!)** to ComfyUI\custom_nodes\ComfyUI_Primere_Nodes\front_end\images\hypernetworks\ path but only the preview images needed, same name as the hypernetwork file but with .jpg only extension.
**If you have hypernetwork files from unknown source, set 'safe_load' switch to true.** With this settings sometime your hypernetwork settings will be ignored, but your computer stay safe.
As extra features you can enable/disable modal with 'show_modal' switch, and exclude files and paths from modal starts with . (point) character if show_hidden switch is off.

<a href="./Workflow/readme_images/pvhyper.jpg" target="_blank"><img src="./Workflow/readme_images/pvhyper.jpg" height="200px"></a>
<hr>

### Primere Visual Style selector:
Same as than the 'Primere Styles' node, but with preview images of selection modal.  
You must create .jpg images as preview with same name as the style name in the list, but **space characters must be changed to _.** For example if your style in the list is 'Architechture Exterior', you must save Architechture_Exterior.jpg to the path: ComfyUI\custom_nodes\ComfyUI_Primere_Nodes\front_end\images\styles\
The styles.example.csv included, if you rename to styles.csv you will see example previews, and you can insert your own custom prompts to styles.csv.

<a href="./Workflow/readme_images/pvstyles.jpg" target="_blank"><img src="./Workflow/readme_images/pvstyles.jpg" height="300px"></a>
<hr>

## Submenu :: Segments:
Under this submenu you can found nodes for detailer/refiner nodes, and required one more **Primere Refiner Prompt** node from the Inputs menu. 
For these nodes you have to download ultralitics bbox and segmentation models from here: https://huggingface.co/Bingsu/adetailer/tree/main or use Comfy's internal model downloader (this is much easier).
Have to save these models to ComfyUI\models\ultralytics\segm\ and ComfyUI\models\ultralytics\bbox\ paths, the Comfy model manager save these models to right path automatically. For the included workflow these models required, but maybe you don't need all models if created your own custom workflow.

#### Download files manually from here:
- Universal segmentation model, useful labels included to node: https://huggingface.co/ultralyticsplus/yolov8s/tree/main
- Important and useful model set: https://huggingface.co/jags/yolov8_model_segmentation-set/tree/main
- Another link for example for deepfashion: https://huggingface.co/Bingsu/adetailer/tree/main
- Segmentation models for anime/cartoon: https://huggingface.co/RamRom/yolov8m_crop-anime-characters/tree/main, https://huggingface.co/AkitoP/Anime-yolov8-seg/tree/main
- Segment anything: https://huggingface.co/ybelkada/segment-anything/tree/main/checkpoints
- But the best if you use Comfy's model manager to download required models, use manual download if you nees something else

<hr>

### WARNING: The "Image Segments" node will download all required segmentation models to the right path if not exist. This cause long loading time at first start (about ~10 minutes) depending on network speed, and required ~6.5 GB of disk space

<hr>

### Tips for use detailer nodes:
- For hands, faces, persons, hair and skins just use specific models without labels (keywords). 
- Another contents, for example cars or animals use universal model like **yolov8s** and don't forget to select right label from bottom list.
- Large faces don't need refiner or detailer because just change the good face to another one (or crerating new worst). If you create closeup portrait, just switch off (or trigger by size) the face detailer.
- On large faces, for example portrait, good idea to refine eyes and mouth only. These refiners can be on, while the face detailer off (or off automatically by trigger values).
- Finally you can use hand detailer. Depending on settings, this group will refine smaller hands too. 
- For cartoon/anime use anime segmentation models, what very different I use and recommended.  
- Check (and modify) refiners's prompts. That very important, and you can mix this prompt to original for several results.
- If you set **strength** of prompts to **0** on **Primere Refiner Prompt** node, the prompt input will be ignored. Not always good idea to mix detailer's prompt to the original, but you don't need to remove original connection, you can set strenght value to 0, same as disconnect.
- Not too easy to set really good refiner group, the result depending on source image and node stttings. All settings will drastically modify the result with same prompt and seed.
- You can use standard dynamic prompts within the Refiner prompt node.
- Try to use **trigger values** to automatically on/off the detailer by the segmented area. Read later on the **Primere Image Segments** node.

<hr>

#### For smaller faces you need face detailer, but don't need eye and mouth detailers:
<a href="./Workflow/readme_images/pdetsmallfaces.jpg" target="_blank"><img src="./Workflow/readme_images/pdetsmallfaces.jpg" height="210px"></a>

#### For half-body or closeup partraits you don't need face detailer, but need eye and mouth detailers:
<a href="./Workflow/readme_images/pdetlargefaces.jpg" target="_blank"><img src="./Workflow/readme_images/pdetlargefaces.jpg" height="270px"></a>

<hr>

### Primere Image Segments:
This node select segs and bbox model, but for three models: **yolov8s**, **deepfashion2_yolov8s** and **facial_features_yolo8x** you must select keyword label too. When you use one of these models with right label selection, the segmentation result will folow your selected label.
Another models no need label. You can use these nodes for workflow result by new prompts, but you can use if the input is existing image only. Load/test attached **civitai-[what]-refiner.json** workflows how to use these nodes if you want to refine your existing images.
You can On/Off this node anytime by switch and **triggers**, and you can play with available parameters.

#### Triggers:
Two trigger input available on this node, **trigger_high_off** and **trigger_low_off**. These input fields are numerical inputs, mean the percentage of original image area. For example 10 in trigger mean, the segmented area is the 10 percent of original image. Both are designed to automatically switch on/off the node by the area of segmented image.
The good trigger value depending on the segmented area compare to the source image. If you want to ignore segments smaller than 5% of input image, add 5 to **trigger_low_off** input, and segments under 5% of original pixels will be ignored. This is useful if the segment (for example mouth) too small to do correct refining.
The **trigger_high_off** switch off the node if the segmented area higher percent than this field value. For example if the face is always good if larger than 10 percent of original image area, enter 10 to the **trigger_high_off** input, and the node will pricess segments only if the segmented area less than 10% of original.
In the example workflow for face detailers I using trigger_high_off = 1, because if the area of segmented face less than 1%, then I need the node for fix small faces. If larger than 1%, no need fixes because usually good enought. The right value depending on used model, prompt, and additional networks like Loras or controlnet settings.
For mouth I using trigger_low_off = 0.25, because if the area of mouth less than 0.25%, no need to repair, only if larger.
For hand fixer I set trigger_high_off to 5, because if the hand's area is larger than 5%, usually no need to fix/detail. All settings depending in workflow settings and the input image.

<a href="./Workflow/readme_images/pimgsegments.jpg" target="_blank"><img src="./Workflow/readme_images/pimgsegments.jpg" height="350px"></a>

### This node will download all required segmentation models to the right path, if models not exist. This is long loading time (about ~10 minutes), and required ~6.5 GB of disk space  

<hr>

### Primere Any Detailer:
This node create detailed/refined output by input image and segs. Node must be used together with Image Segments and Refiner Prompt. The output of this node can be upscaled or saved, maybe connected to the next refiner.
Detailer group exaple included to the **Primere_latest_workflow.json** you can to check it for your own ideas and settings, or test only detailers in attached **civitai-[what]-refiner.json** files.

#### Detailer automatically handle Normal, LCM and Turbo model concepts if the 'model_concept' and 'concept_*' nodes used. Check the Primere_latest_workflow how to automatically control this node for all 3 concepts. Fpr normal mode, you can set samples to anything else, different from the original image creation settings.

<a href="./Workflow/readme_images/panydetailer.jpg" target="_blank"><img src="./Workflow/readme_images/panydetailer.jpg" height="380px"></a>
<hr>

## Submenu :: Inputs:

### Primere Prompt:
2 input fileds within one node for positive and negative prompts. 3 additional fields appear under the text inputs:
- **Subpath**: the prefered subpath for final image saving. This can be use for example the subject of the generated image, like 'sci-fi' 'art' or 'interior'. This setting overwrite the subpath setting in 'Primere Image Meta Saver' node.
- **Use model**: the prefered checkpoint for image rendering. If your prompt need special checkpoint, for example because product design or architechture, here you can force apply this model to the prompt rendering process. This setting overwrite dashboard settings.
- **Use orientation**: if you prefer vertical or horizontal orientation depending on your prompt, your rendering process will be use this setting instead of global setting from 'Primere Resolution' node. Useful for example for portraits, what usually better in vertical orientation. Random settings available here, use with batch mode if you need several orientations for same prompt.

If you set these fields, (where 'None' mean not set and use dashboard settings) the workflow will use all of these settings for rendering your prompt instead of settings in 'Dashboard' group.

<a href="./Workflow/readme_images/pprompt.jpg" target="_blank"><img src="./Workflow/readme_images/pprompt.jpg" height="130px"></a>
<hr>

### Primere Styles:
Style (.csv) file reader, compatible with A1111 syles.csv, but little more than the original concept. The file must be copied/symlinked to the 'stylecsv' folder. Rename included 'style.example.csv' to 'style.csv' for first working example, and later edit this file manually.
- **A1111 compatible CSV headers required for this file**: 'name,prompt,negative_prompt'. But this version have more 3 required headers: 'prefered_subpath,prefered_model,prefered_orientation'. These new headers working like additional fields in the simple prompt input. 
- If you fill these 3 optional columns in the style.csv, the rendering process will use them. **These last 3 fields are optional**, if you leave empty the style will be rendering with system 'dashboard' settings, if fill and enable to use at the bottom switches of node, dashboard settings will be overwritten.
- You can enable/disable these additional settings by switches if already entered to csv but want to use system settings instead, no need to delete if you failed or want to try with dashboard settings instead.

<a href="./Workflow/readme_images/pstyles.jpg" target="_blank"><img src="./Workflow/readme_images/pstyles.jpg" height="120px"></a>
<hr>

### Primere Prompt Organizer
Prompts and additional data must be stored in the .toml file. This node dynamically read and organize the custom file content. The example file with data schema is on the path **Toml/prompts.example.toml**, just rename to the **prompts.toml** end edit/include your own prommpt.
- [HEADER_NAME] is the main header.
- [HEADER_NAME.N_x] it the second level header. The string after dor 'N_x' is not important, but must be unique under same first level header, where the 'x' is an unique number.
- **prefered_subpath** optional data, if 'use_subpath' is true on the node, the image saver will use this string as subdirectory.
- **Name** required data for prompt list combo.
- **prefered_model** optionald ata, if you have 'must use' model for the prompt.
- **prefered_orientation** optional data, if you prefer vertical or horizontal orientation for your prompt.
- **Positive** required, the positive prompt.
- **Negative** optional, the negative prompt.

Follow the file schema for your own prompts but don't forget to rename the attached example file to prompts.toml.

<a href="./Workflow/readme_images/ppromptorganizer.jpg" target="_blank"><img src="./Workflow/readme_images/ppromptorganizer.jpg" height="220px"></a>
<hr>

### Primere Dynamic:
- This node render A1111 compatible dynamic prompts, including external wildcard files of A1111 dynamic prompt plugin. External files must be copied/symlinked to the 'wildcards' folder and use the '__filepath/of/file__' keyword within your prompt. Use this to decode all style.csv and double prompt inputs, because the output of prompt/style nodes not resolved by another comfy dynamic decoder/resolver.
- Check the included workflow how to use this node.

<a href="./Workflow/readme_images/pdynamic.jpg" target="_blank"><img src="./Workflow/readme_images/pdynamic.jpg" height="80px"></a>
<hr>

### Primere exif reader:
- This node read prompt-exif (called meta) from loaded image. Compatible with A1111 .jpg and .png, and usually with ComfyUI, but not with results of all other custom workflows.
- This is important (the most important) node in the attached 'Primere_latest_workflow.json' workflow, it has a central settings distribution role, not just read the exif data.
- The reader is tested with A1111 'jpg' and 'png' and Comfy 'jpg' and 'png'. Another exif parsers will be included soon, but if you send me AI generated image contains exif/metadata what failed to read, I will do parser/debug for that.

This node output sending lot of data to the workflow from exif/meta or pnginfo if it's included to selected image, like model name, vae and sampler name or settings. Use this node to distribute settings, and simple off the 'use_exif' switch if you don't want to render image by this node, then you can use your own prompts and dashboard settings instead.

**Use several settings of switches what exif/meta data you want/don't want to use for new image rendering.** If switch off something, dashboard settings (this is why must be connected this node input) will be used instead of image included exif/meta.
#### For this node inputs connect all of your dashboard settings, like in the example workflow. If you switch off the exif reader with 'use_exif' switch, or ignore specified data for example the model, the input values will be used instead of image meta. The example workflow help to analize how to use this node.

<a href="./Workflow/readme_images/pexif.jpg" target="_blank"><img src="./Workflow/readme_images/pexif.jpg" height="250px"></a>
<hr>

### Primere Embedding Handler:
This node convert A1111 embeddings to Comfy embeddings. Use after dynamically decoded prompts (booth text and style). **No need to modify manually styles.csv from A1111 if you use this node.**

<a href="./Workflow/readme_images/pemhandler.jpg" target="_blank"><img src="./Workflow/readme_images/pemhandler.jpg" height="80px"></a>
<hr>

### Primere Lora Stack Merger:
This node merge two different Lora stacks, SD and SDXL. The output is useful to store Lora settings to the image meta.
<hr>

### Primere Lora Keyword Merger:
With Lora stackers you can read model keywords. This node merge all selected Lora keywords to one string, and send to prompt encoder.
<hr>

### Primere Lycoris Stack Merger:
This node merge two different Lycoris stacks, SD and SDXL. The output is useful to store Lycoris settings to the image meta.
<hr>

### Primere Lycoris Keyword Merger:
With Lycoris stackers you can read model keywords. This node merge all selected Lycoris keywords to one string, and send to prompt encoder.
<hr>

### Primere Embedding Keyword Merger:
This node merge positive and negative SD and SDXL embedding tags, to send them to the prompt encoder.
<hr>

### Primere VAE selector:
This node select between SD and SDXL VAE if model_version input is correct.

<a href="./Workflow/readme_images/pvaeselector.jpg" target="_blank"><img src="./Workflow/readme_images/pvaeselector.jpg" height="80px"></a>
<hr>

### Primere Refiner Prompt:
Another dual prompt input, bur for refiners and detailers. You can connect original prompts too to this node, and set the weights of all inputs. Text and cond outputs are available.
For more info about usage see **"Segments"** submenu.

<a href="./Workflow/readme_images/prefprompt.jpg" target="_blank"><img src="./Workflow/readme_images/prefprompt.jpg" height="200px"></a>
<hr>

## Submenu :: Dashboard:
### Primere Sampler Selector:
Select sampler and scheduler in separated node, and wire outputs to the sampler (through exif reader input in the example workflow). This is useful to separate from other nodes, and for LCM and Turbo modes you need three several sampler settings. (see the example workflow, and try to undestand LCM and Turbo setting)

<a href="./Workflow/readme_images/psampler.jpg" target="_blank"><img src="./Workflow/readme_images/psampler.jpg" height="80px"></a>
<hr>

### Primere Steps & Cfg:
Use this separated node for sampler/meta reader inputs. If you use LCM and Turbo modes, you need 3 with several settings of this node. See and test the attached example workflow.

<a href="./Workflow/readme_images/psteps.jpg" target="_blank"><img src="./Workflow/readme_images/psteps.jpg" height="80px"></a>
<hr>

### Primere Samplers & Steps & Cfg:
Use this separated node for sampler/meta reader inputs. If you use LCM and Turbo modes, you need 3 with different settings of this node. See and test the attached example workflow.
This node the merged version of previous two: 'Primere Sampler Selector' and 'Primere Steps & Cfg'

<a href="./Workflow/readme_images/psamcfgsel.jpg" target="_blank"><img src="./Workflow/readme_images/psamcfgsel.jpg" height="140px"></a>
<hr>

### Primere LCM Selector:
Use this node to switch on/off LCM mode in whole rendering process. Wire two sampler and cfg/steps settings to the inputs (one of them must be compatible with LCM settings), and connect this node output to the sampler/exif reader, like in the example workflow. The 'IS_LCM' output important for CKPT loader and the Exif reader for correct rendering.

<a href="./Workflow/readme_images/plcm.jpg" target="_blank"><img src="./Workflow/readme_images/plcm.jpg" height="150px"></a>
<hr>

### Primere Model Concept Selector:
Use this node to switch between Normal, LCM and Turbo modes in whole rendering process. Wire three sampler and cfg/steps settings to the inputs (one of them must be compatible with LCM settings, another must flow Turbo rules), and connect this node output to the sampler/exif reader, like in the example workflow. The 'MODEL_CONCEPT' output important for CKPT loader, Image refiners, and the Exif reader for correct rendering.

<a href="./Workflow/readme_images/pmodelconcept.jpg" target="_blank"><img src="./Workflow/readme_images/pmodelconcept.jpg" height="240px"></a>
<hr>

### Primere VAE Selector:
This node is a simple VAE file selector. Use 2 nodes in workflow, 1 for SD, 1 for SDXL compatible VAE for autimatized selection.
<hr>

### Primere CKPT Selector:
Simple checkpoint selector, but with extras:
- This node automatically detect if the selected model SD or SDXL. Use this output for automatic VAE, additional networks or size selection and for prompt encoding, see example workflow for details.
- Check the "visual" version of this node, if you already have previews for checkpoints, easier to select the best for your prompt. How to create preview for visual selection, read later on this readme.

<a href="./Workflow/readme_images/pckptselect.jpg" target="_blank"><img src="./Workflow/readme_images/pckptselect.jpg" height="80px"></a>
<hr>

### Primere VAE loader:
Use this node to convert VAE name to VAE.
<hr>

### Primere CKPT Loader:
Use this node to convert checkpoint name to 'MODEL', 'CLIP' and 'VAE'. Use 'model_concept' input for detect LCM and Turbo modes, see the example workflow.
If you have downloaded .yaml file, and copied to the checkpoint's directory with same filename, set 'use_yaml' to true, and the loader will use read and use the config file. No need to swithc off if .yaml file missing. If you find some problem or error, simply set it to false.
Play with 'strength_lcm_model' and 'strength_lcm_clip' values if set LCM mode on whole workflow.
This node have optional inputs if checkpoint already loaded by previous process. If 'loaded_clip', 'loaded_vae' and 'loaded_model' connected, this node will use these inputs instead of loading checkpoint again. 

<a href="./Workflow/readme_images/pckpt.jpg" target="_blank"><img src="./Workflow/readme_images/pckpt.jpg" height="150px"></a>
<hr>

### Primere Prompt Switch:
Use this node if you have more than one prompt input (for example several half-ready test or development prompts). Connect prompts/styles node outputs to this node inputs and set the right index at the bottom. To connect 'subpath', 'model', and 'orientation' inputs are optional, only the positive and negative prompt required.

**Very important:** don't remove the connected node from the middle or from the top of inputs. Connect nodes in right queue, and disconnect them only from the last to first. If you getting js error becuase disconnected inputs in wrong gueue, just reload your browser and use 'reload node' menu with right click on node.

<a href="./Workflow/readme_images/prpmptswitch.jpg" target="_blank"><img src="./Workflow/readme_images/prpmptswitch.jpg" height="150px"></a>
<hr>

### Primere Seed:
Use only one seed input for all. A1111 look node, connect this one node to all other seed inputs.

<hr>

### Primere Noise Latent:
This node generate 'empty' latent image, but with several noise settings, what control the final images. **You can randomize these setting between min. and max. values using switches**, this cause small difference between generated images for same seed and settings, but you can freeze your noise and latent image if you disable variations of random noise generation.
- You can generate several images with large difference with randomized dashboard seed
- If you freeze seed (on the dashboard group) and set the min and max values of generation details on this node, you will get small differences by your noise values (primary by alpha_exponent and modulator if randomized)
- If the difference not big enought switch on 'extra_variation' and set 'control_after_generate' to 'randomize' or 'increment' or 'decrement'. You can get different but consistent images with these settings **if the dasboard seed locked** 

<a href="./Workflow/readme_images/platent.jpg" target="_blank"><img src="./Workflow/readme_images/platent.jpg" height="240px"></a>
<hr>

### Primere Prompt Encoder:
- This node compatible booth SD and SDXL models, important to use 'model_version' (SD, SDXL) and 'model_concept' (Normal, LCM, Turbo) inputs for correct working. Try several settings, you will get several results. 
- Use included positive and negative styles, and check the best result in prompt and image outputs. 
- If you getting error if use SD basemodel, you must update (git pull) your ComfyUI.
- The style source of this node in external file at 'Toml/default_neg.toml' and 'Toml/default_pos.toml' files, what you can edit if you need changes.
- Connect here the additional network keywords like in the example workflow.

<a href="./Workflow/readme_images/pencoder.jpg" target="_blank"><img src="./Workflow/readme_images/pencoder.jpg" height="320px"></a>
<hr>

### Primere Resolution:
- Select image size by side ratios only, and use 'model_version' and 'model_concept' inputs for correct SD, SDXL - Normal - Turbo size on the output.  
- You can calculate image size by custom ratios at the bottom float inputs (and set 'calculate_by_custom' switch on), or just edit the external ratio source file.
- The ratios of this node stored in external file at 'Toml/resolution_ratios.toml', what you can edit if you need changes.
- Use 'round_to_standard' switch if you want to modify the exactly calculated size to the 'officially' recommended SD / SDXL values. This is usually very small modification and I think not too important, but some 3rd party nodes failed if the side not divisible by 16.
- Not sure what orientation the best for your prompt and want to test in batch image generation? Just set batch value on the Comfy menu and switch 'rnd_orientation' to randomize vertical and horizontal images.
- Set the model basse resolution to 512, 768, 1024, 1280, 1600, or 2048, both SD, SDXL and Turbo, but in separated inputs. The official setting is 512 SD, but I like 768 instead, and 1024 for SDXL. The Turbo resolution depending on your use model.

<a href="./Workflow/readme_images/pres.jpg" target="_blank"><img src="./Workflow/readme_images/pres.jpg" height="180px"></a>
<hr>

### Primere Resolution Multiplier:
Multiply the base image size for upscaling. Important to use 'model_version' and 'model_concept' if you want to use several multipliers for Turbo, SD and SDXL models. Just switch off 'use_multiplier' on this node if you don't need to resize the original image.

If your upscaler failed becuse low memory error, try to switch on 'triggered_prescale' and set right values to the input fields under this switch. This function resize the source image before upscaling to right size:

- **area_trigger_mpx:** the value of the image area in megapixels when the 'pre-scale' process run. For example if your original image based on 512px, the source image area in megapixels = 0.26. If you set this value to 0.55, your 512 based images will be processed, but 768 (0.58 mpx) and larger pictures will be ignored.
- **area_target_mpx:** the value to resize the source image before sending to the upscaler in megapixels. If you use this function, and for example want to upscale your 512 based image to 6-8 times larger but the upscaler failed, resize the source to 2mpx (or 3mpx) before upscaling.
- **upscale_model:** set the upscale model instead of interpolation (upscale_method input). **Warning: the selected upscale model will resize your source image by fix ratio. For example '4x-UltraSharp' will resize you image by ratio 4 to 4 times larger.**
- **upscale_method:** if you don't want to use upscale_model, what mean set the previous combo to 'None', here you can seleect the interpolation method, the source image will be resize to the value of 'area_target_mpx' input.

<a href="./Workflow/readme_images/presmul.jpg" target="_blank"><img src="./Workflow/readme_images/presmul.jpg" height="200px"></a>
<hr>

### Primere Resolution MPX:
Multiply the base image size for upscaling. This node upscale original images to the value of megapixels (upscale_to_mpx). No need to use model concepts or versions, just the original image size needed. Just switch off 'use_multiplier' on this node if you don't need to resize the original image.

If your upscaler failed becuse low memory error, try to switch on 'triggered_prescale' and set right values to the input fields under this switch. This function resize the source image before upscaling to right size:

- **area_trigger_mpx:** the value of the image area in megapixels when the 'pre-scale' process run. For example if your original image based on 512px, the source image area in megapixels = 0.26. If you set this value to 0.55, your 512 based images will be processed, but 768 (0.58 mpx) and larger pictures will be ignored.
- **area_target_mpx:** the value to resize the source image before sending to the upscaler in megapixels. If you use this function, and for example want to upscale your 512 based image to 10-12 megapixels or larger but the upscaler failed, resize the source to 2 mpx (or 3-4 mpx) before upscaling.
- **upscale_model:** set the upscale model instead of interpolation (upscale_method input). **Warning: the selected upscale model will resize your source image by fix ratio. For example '4x-UltraSharp' will resize you image by ratio 4 to 4 times larger.**
- **upscale_method:** if you don't want to use upscale_model, what mean set the previous combo to 'None', here you can seleect the interpolation method, the source image will be resize to the value of 'area_target_mpx' input.

<a href="./Workflow/readme_images/presmulmpx.jpg" target="_blank"><img src="./Workflow/readme_images/presmulmpx.jpg" height="180px"></a>
<hr>

### Primere Prompt Cleaner:
This node remove Lora, Lycoris, Hypernetwork and Embedding (booth A1111 and Comfy) from the prompt and style inputs. Use switches what netowok(s) you want to remove or keep in the final prompt. Use 'remove_only_if_sdxl' if you want keep all of these networks for SD1.5 models, and remove only if SDXL checkpoint selected.
**Important notice:** for loras, lycoris and hypernetworks you don't need original tags in the prompt (for example: \<lora:your_lora_name>). If you keep original lora and hypernetwork tags in the prompt you cant sure your image result use the lora only, or use the tag string only (or booth) in the prompt. I recommend always to remove lora and hypernetwork tags, but you can try what happan if keep.
You must remove original tags after 'Primere Network Tag Loader', because after prompt cleaner no tags available for tag loader. The example workflow using 2 of this nodes, one for SD, one for SDXL workflow.

<a href="./Workflow/readme_images/ppcleaner.jpg" target="_blank"><img src="./Workflow/readme_images/ppcleaner.jpg" height="120px"></a>
<hr>

### Primere Network Tag Loader
This node loads addtional networks (Lora, Lycoris and Hypernetwork) to the CLIP and MODEL. You can read and use Lora (lora:[your model name]), Lycoris (lyco:[your model name]) and Hypernetwork (hypernetwork:[your model name]) keywords to send to prompt encoder or the keyword merger like in the example workflow.
**Hypernetwork is harmful, because can run any code on your computer, so set 'process_hypernetwork' to False on this node or download them from reliable source only**
**If you have hypernetwork files from unknown source, set 'safe_load' switch to true.** With this settings sometime your hypernetwork tags will be ignored, but your computer stay safe.

<a href="./Workflow/readme_images/pnettagload.jpg" target="_blank"><img src="./Workflow/readme_images/pnettagload.jpg" height="200px"></a>
<hr>

### Primere Model Keyword
This node loads model keyword. You can read and use model keywords to send directly to prompt encoder like in the example workflow. The idea based on A1111 plugin, but something different.

<a href="./Workflow/readme_images/pmodkeyw.jpg" target="_blank"><img src="./Workflow/readme_images/pmodkeyw.jpg" height="100px"></a>
<hr>

## Submenu :: Outputs:

### Primere Meta Saver:
This node save the image, but with/without metadata, and save meta to .json/.txt file if you want. Get metadata from the Exif reader node only, and use optional 'prefered_subpath' input if you want to overwrite the node settings by several prompt input nodes. Set 'output_path' input correctly, depending your system.

<a href="./Workflow/readme_images/pimgsaver.jpg" target="_blank"><img src="./Workflow/readme_images/pimgsaver.jpg" height="200px"></a>
<hr>

### Primere Any Debug:
Use this node to display 'any' output values of several nodes like prompts or metadata (**metadata is formatted**). See the example workflow for details.
<hr>

### Primere Text Output:
Use this node to diaplay simple text (not tuples or dict).
<hr>

### Primere Meta Collector:
Use this node in the workflow if you don't need Primere Meta Reader node. This node collect required metadata for Primere Meta Saver, the data will be stored to .jpg exif or .png pnginfo, then you can read back and recycle your previous prompts and settings by Primere Meta Reader. Check 'Primere_advanced_workflow.json' how to use this node.

<a href="./Workflow/readme_images/pmetacoll.jpg" target="_blank"><img src="./Workflow/readme_images/pmetacoll.jpg" height="250px"></a>
<hr>

### Primere KSampler:
KSampler, no difference between this node and Comfy's KSampler, but by the 'model_concept' input this node automatically handle Turbo mode, no need another workflow or node.

<a href="./Workflow/readme_images/pksampler.jpg" target="_blank"><img src="./Workflow/readme_images/pksampler.jpg" height="220px"></a>
<hr>

## Submenu :: Styles:
### Primere Style Pile:
Style collection for generated images. Set and connect this node to the 'Prompt Encoder'. No forget to set and play with style strenght. The source of this node is external file at 'Toml/stylepile.toml', what you can edit if you need changes.

<a href="./Workflow/readme_images/pstylepile.jpg" target="_blank"><img src="./Workflow/readme_images/pstylepile.jpg" height="200px"></a>
<hr>

### Primere Midjourney Styles:
Style collection from Midjourney. You can attach art-style prompt to your original prompt, and get your result in several artistic style.

<a href="./Workflow/readme_images/pmidjourney.jpg" target="_blank"><img src="./Workflow/readme_images/pmidjourney.jpg" height="340px"></a>

Example images about the result of this style node. The left-top image is the original without any style, all others styled by this one, using SD1.5 model, same seed, same prompt:

<a href="./Workflow/readme_images/mjmontage.jpg" target="_blank"><img src="./Workflow/readme_images/mjmontage.jpg" height="300px"></a>

<hr>

### Primere Emotions Styles:
Style collection of emotions. You can attach emotion-style to your original prompt, and get your result in several emotion style. The source content will be update frquently to more emotions.

<a href="./Workflow/readme_images/pstyleemo.jpg" target="_blank"><img src="./Workflow/readme_images/pstyleemo.jpg" height="280px"></a>

Example images about the result of this style node. The left-top image is the original without any style, all others styled by this one, using SDXL model, same seed, same prompt:

<a href="./Workflow/readme_images/emomontage.jpg" target="_blank"><img src="./Workflow/readme_images/emomontage.jpg" height="300px"></a>

<hr>

## Submenu :: Networks:
### Primere LORA
Lora stack for 6 loras. Important to use 'stack_version' list. Here you can select how you want to load selected Lora-s, for SD models only, for SDXL models only or for booth (Any) what not recommended. Use 2 separated Lora stacks for SD/SDXL checkpoints, and wire 'model_version' input for correct use.
- You can switch on/off loras, no need to choose 'None' from the list.
- If you use 'use_only_model_weight', the model_weight input values will be copied to clip_weight.
- If you switch off 'use_only_model_weight', you can set model_weight and clip_weight to different values.
- You can load and send to Prompt Encoder the Lora keyword if available. This is similar but not exactly same function of "Model Keyword" plugin in the A1111.
- You can choose Lora keyword placement, which and how many keywords select if more than one available, how many keyword use if more than one available, select in queue or random, and set the keyword weight in the prompt.
- Lora keyword is much better than to keep lora tag in the prompt.

<a href="./Workflow/readme_images/plora.jpg" target="_blank"><img src="./Workflow/readme_images/plora.jpg" height="200px"></a>
<hr>

### Primere LYCORIS
Lycoris files have dedicated node, wirking similar than the LORA stack. See example workflow, or use as LORA.
If you already have downloaded LyCORIS files, you must simlynk or copy to the path **ComfyUI\models\lycoris\**. I remcommend simlynk the original source instead of copyying.

<a href="./Workflow/readme_images/plyco.jpg" target="_blank"><img src="./Workflow/readme_images/plyco.jpg" height="200px"></a>
<hr>

### Primere Embedding
Select textual inversion called Embedding for your prompt. You have to use 2 several versions of this one, one for SD, and another one for SDXL checkpoints. Important to use 'model_version' input and 'stack_version' list, working similar than in the Lora stack. 
You can choose embedding placement in the prompt.

<a href="./Workflow/readme_images/pembed.jpg" target="_blank"><img src="./Workflow/readme_images/pembed.jpg" height="200px"></a>
<hr>

### Primere Hypernetwork
Use hypernetwork if you already have by this node. **Hypernetwork is harmful, because can run any code on your computer, so ignore/delete this node or download them from reliable source only**
**If you have hypernetwork files from unknown source, set 'safe_load' switch to true.** With this settings sometime your hypernetwork settings will be ignored, but your computer stay safe.
Hypernetworks don't need seperated SD and SDXL sources, use only one stack for all, and set 'stack_version' to 'Any'. 

<a href="./Workflow/readme_images/phyper.jpg" target="_blank"><img src="./Workflow/readme_images/phyper.jpg" height="200px"></a>
<hr>

# Contact:
#### Discord name: primere -> ask email if you need or use git for fork and pull request

# Licence:
#### Use these nodes for your own risk