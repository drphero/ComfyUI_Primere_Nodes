from ..components.tree import TREE_NETWORKS
from ..components.tree import PRIMERE_ROOT
import folder_paths
from ..components import utility
from ..components import hypernetwork
import comfy.sd
import comfy.utils
import os
import random
from pathlib import Path
from ..utils import comfy_dir
# import comfy_extras.nodes_hypernetwork as comfy_extras

class PrimereLORA:
    RETURN_TYPES = ("MODEL", "CLIP", "LORA_STACK", "MODEL_KEYWORD")
    RETURN_NAMES = ("MODEL", "CLIP", "LORA_STACK", "LORA_KEYWORD")
    FUNCTION = "primere_lora_stacker"
    CATEGORY = TREE_NETWORKS
    LORASCOUNT = 6

    @classmethod
    def INPUT_TYPES(cls):
        LoraList = folder_paths.get_filename_list("loras")

        return {
            "required": {
                "model": ("MODEL",),
                "clip": ("CLIP",),
                "model_version": ("STRING", {"default": 'BaseModel_1024', "forceInput": True}),
                "stack_version": (["SD", "SDXL", "Any"], {"default": "Any"}),
                "use_only_model_weight": ("BOOLEAN", {"default": True}),

                "use_lora_1": ("BOOLEAN", {"default": False}),
                "lora_1": (LoraList,),
                "lora_1_model_weight": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),
                "lora_1_clip_weight": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),

                "use_lora_2": ("BOOLEAN", {"default": False}),
                "lora_2": (LoraList,),
                "lora_2_model_weight": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),
                "lora_2_clip_weight": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),

                "use_lora_3": ("BOOLEAN", {"default": False}),
                "lora_3": (LoraList,),
                "lora_3_model_weight": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),
                "lora_3_clip_weight": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),

                "use_lora_4": ("BOOLEAN", {"default": False}),
                "lora_4": (LoraList,),
                "lora_4_model_weight": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),
                "lora_4_clip_weight": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),

                "use_lora_5": ("BOOLEAN", {"default": False}),
                "lora_5": (LoraList,),
                "lora_5_model_weight": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),
                "lora_5_clip_weight": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),

                "use_lora_6": ("BOOLEAN", {"default": False}),
                "lora_6": (LoraList,),
                "lora_6_model_weight": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),
                "lora_6_clip_weight": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),

                "use_lora_keyword": ("BOOLEAN", {"default": False}),
                "lora_keyword_placement": (["First", "Last"], {"default": "Last"}),
                "lora_keyword_selection": (["Select in order", "Random select"], {"default": "Select in order"}),
                "lora_keywords_num": ("INT", {"default": 1, "min": 1, "max": 50, "step": 1}),
                "lora_keyword_weight": ("FLOAT", {"default": 1.0, "min": 0, "max": 10.0, "step": 0.1}),
            },
        }

    def primere_lora_stacker(self, model, clip, use_only_model_weight, use_lora_keyword, lora_keyword_placement, lora_keyword_selection, lora_keywords_num, lora_keyword_weight, stack_version = 'Any', model_version = "BaseModel_1024", **kwargs):
        model_keyword = [None, None]

        if model_version == 'SDXL_2048' and stack_version == 'SD':
            return (model, clip, [], model_keyword)

        if model_version != 'SDXL_2048' and stack_version == 'SDXL':
            return (model, clip, [], model_keyword)

        loras = [kwargs.get(f"lora_{i}") for i in range(1, self.LORASCOUNT + 1)]
        model_weight = [kwargs.get(f"lora_{i}_model_weight") for i in range(1, self.LORASCOUNT + 1)]
        if use_only_model_weight == True:
            clip_weight =[kwargs.get(f"lora_{i}_model_weight") for i in range(1, self.LORASCOUNT + 1)]
        else:
            clip_weight =[kwargs.get(f"lora_{i}_clip_weight") for i in range(1, self.LORASCOUNT + 1)]

        uses = [kwargs.get(f"use_lora_{i}") for i in range(1, self.LORASCOUNT + 1)]
        lora_stack = [(lora_name, lora_model_weight, lora_clip_weight) for lora_name, lora_model_weight, lora_clip_weight, lora_uses in zip(loras, model_weight, clip_weight, uses) if lora_uses == True]

        lora_params = list()
        if lora_stack and len(lora_stack) > 0:
            lora_params.extend(lora_stack)
        else:
            return (model, clip, lora_stack, model_keyword)

        model_lora = model
        clip_lora = clip
        list_of_keyword_items = []
        lora_keywords_num_set = lora_keywords_num

        for tup in lora_params:
            lora_name, strength_model, strength_clip = tup

            lora_path = folder_paths.get_full_path("loras", lora_name)
            lora = comfy.utils.load_torch_file(lora_path, safe_load=True)
            model_lora, clip_lora = comfy.sd.load_lora_for_models(model_lora, clip_lora, lora, strength_model, strength_clip)

            loraname_only = Path(lora_name).stem
            model_lora_version = utility.get_value_from_cache('lora_version', loraname_only)
            if model_lora_version is None:
                loraVER = utility.getLoraVersion(lora)
                if loraVER is not None:
                    utility.add_value_to_cache('lora_version', loraname_only, loraVER)

            if use_lora_keyword == True:
                ModelKvHash = utility.get_model_hash(lora_path)
                if ModelKvHash is not None:
                    KEYWORD_PATH = os.path.join(PRIMERE_ROOT, 'front_end', 'keywords', 'lora-keyword.txt')
                    keywords = utility.get_model_keywords(KEYWORD_PATH, ModelKvHash, lora_name)
                    if keywords is not None and keywords != "" and isinstance(keywords, str) == True:
                        if keywords.find('|') > 1:
                            keyword_list = [word.strip() for word in keywords.split('|')]
                            keyword_list = list(filter(None, keyword_list))
                            if (len(keyword_list) > 0):
                                lora_keywords_num = lora_keywords_num_set
                                keyword_qty = len(keyword_list)
                                if (lora_keywords_num > keyword_qty):
                                    lora_keywords_num = keyword_qty
                                if lora_keyword_selection == 'Select in order':
                                    list_of_keyword_items.extend(keyword_list[:lora_keywords_num])
                                else:
                                    list_of_keyword_items.extend(random.sample(keyword_list, lora_keywords_num))
                        else:
                            list_of_keyword_items.append(keywords)

        if len(list_of_keyword_items) > 0:
            if lora_keyword_selection != 'Select in order':
                random.shuffle(list_of_keyword_items)

            list_of_keyword_items = list(set(list_of_keyword_items))
            keywords = ", ".join(list_of_keyword_items)

            if (lora_keyword_weight != 1):
                keywords = '(' + keywords + ':' + str(round(lora_keyword_weight, 1)) + ')'

            model_keyword = [keywords, lora_keyword_placement]

        return (model_lora, clip_lora, lora_stack, model_keyword)

class PrimereEmbedding:
    RETURN_TYPES = ("EMBEDDING", "EMBEDDING", "EMBEDDING_STACK")
    RETURN_NAMES = ("EMBEDDING+", "EMBEDDING-", "EMBEDDING_STACK")
    FUNCTION = "primere_embedding"
    CATEGORY = TREE_NETWORKS
    EMBCOUNT = 6

    @classmethod
    def INPUT_TYPES(self):
        EmbeddingList =folder_paths.get_filename_list("embeddings")

        return {
            "required": {
                "model_version": ("STRING", {"default": 'BaseModel_1024', "forceInput": True}),
                "stack_version": (["SD", "SDXL", "Any"], {"default": "Any"}),

                "use_embedding_1": ("BOOLEAN", {"default": False}),
                "embedding_1": (EmbeddingList,),
                "embedding_1_weight": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01,},),
                "is_negative_1": ("BOOLEAN", {"default": False}),

                "use_embedding_2": ("BOOLEAN", {"default": False}),
                "embedding_2": (EmbeddingList,),
                "embedding_2_weight": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01, },),
                "is_negative_2": ("BOOLEAN", {"default": False}),

                "use_embedding_3": ("BOOLEAN", {"default": False}),
                "embedding_3": (EmbeddingList,),
                "embedding_3_weight": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01, },),
                "is_negative_3": ("BOOLEAN", {"default": False}),

                "use_embedding_4": ("BOOLEAN", {"default": False}),
                "embedding_4": (EmbeddingList,),
                "embedding_4_weight": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01, },),
                "is_negative_4": ("BOOLEAN", {"default": False}),

                "use_embedding_5": ("BOOLEAN", {"default": False}),
                "embedding_5": (EmbeddingList,),
                "embedding_5_weight": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01, },),
                "is_negative_5": ("BOOLEAN", {"default": False}),

                "use_embedding_6": ("BOOLEAN", {"default": False}),
                "embedding_6": (EmbeddingList,),
                "embedding_6_weight": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01, },),
                "is_negative_6": ("BOOLEAN", {"default": False}),

                "embedding_placement_pos": (["First", "Last"], {"default": "Last"}),
                "embedding_placement_neg": (["First", "Last"], {"default": "Last"}),
            },
        }

    def primere_embedding(self, embedding_placement_pos, embedding_placement_neg, stack_version = 'Any', model_version = "BaseModel_1024", **kwargs):
        if model_version == 'SDXL_2048' and stack_version == 'SD':
            return ([None, None], [None, None], [])

        if model_version != 'SDXL_2048' and stack_version == 'SDXL':
            return ([None, None], [None, None], [])

        embedding_pos_list = []
        embedding_neg_list = []

        embeddings = [kwargs.get(f"embedding_{i}") for i in range(1, self.EMBCOUNT + 1)]
        use_embeddings = [kwargs.get(f"use_embedding_{i}") for i in range(1, self.EMBCOUNT + 1)]
        embedding_weight = [kwargs.get(f"embedding_{i}_weight") for i in range(1, self.EMBCOUNT + 1)]
        neg_embedding = [kwargs.get(f"is_negative_{i}") for i in range(1, self.EMBCOUNT + 1)]

        embedding_stack = [(emb_name, emb_weight, is_emb_neg) for emb_name, emb_weight, is_emb_neg, emb_uses in zip(embeddings, embedding_weight, neg_embedding, use_embeddings) if emb_uses == True]
        if embedding_stack is not None and len(embedding_stack) > 0:
            for embedding_tuple in embedding_stack:
                embedd_name_path = embedding_tuple[0]
                embedd_weight = embedding_tuple[1]
                embedd_neg = embedding_tuple[2]
                embedd_name = Path(embedd_name_path).stem

                if (embedd_weight != 1):
                    embedding_sting = '(embedding:' + embedd_name + ':' + str(embedd_weight) + ')'
                else:
                    embedding_sting = 'embedding:' + embedd_name

                if embedd_neg == False:
                    embedding_pos_list.append(embedding_sting)
                else:
                    embedding_neg_list.append(embedding_sting)

        else:
            return ([None, None], [None, None], [])

        embedding_pos_list = list(set(embedding_pos_list))
        embedding_neg_list = list(set(embedding_neg_list))

        if len(embedding_pos_list) > 0:
            embedding_pos = ", ".join(embedding_pos_list)
        else:
            embedding_pos = None
            embedding_placement_pos = None

        if len(embedding_neg_list) > 0:
            embedding_neg = ", ".join(embedding_neg_list)
        else:
            embedding_neg = None
            embedding_placement_neg = None

        return ([embedding_pos, embedding_placement_pos], [embedding_neg, embedding_placement_neg], embedding_stack)

class PrimereHypernetwork:
    RETURN_TYPES = ("MODEL", "HYPERNETWORK_STACK")
    RETURN_NAMES = ("MODEL", "HYPERNETWORK_STACK")
    FUNCTION = "primere_hypernetwork"
    CATEGORY = TREE_NETWORKS
    EMBCOUNT = 6

    @classmethod
    def INPUT_TYPES(s):
        HypernetworkList = folder_paths.get_filename_list("hypernetworks")

        return {"required": {
            "model": ("MODEL",),
            "model_version": ("STRING", {"default": 'BaseModel_1024', "forceInput": True}),
            "safe_load": ("BOOLEAN", {"default": True}),
            "stack_version": (["SD", "SDXL", "Any"], {"default": "Any"}),

            "use_hypernetwork_1": ("BOOLEAN", {"default": False}),
            "hypernetwork_1": (HypernetworkList, ),
            "hypernetwork_1_weight": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),

            "use_hypernetwork_2": ("BOOLEAN", {"default": False}),
            "hypernetwork_2": (HypernetworkList,),
            "hypernetwork_2_weight": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),

            "use_hypernetwork_3": ("BOOLEAN", {"default": False}),
            "hypernetwork_3": (HypernetworkList,),
            "hypernetwork_3_weight": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),

            "use_hypernetwork_4": ("BOOLEAN", {"default": False}),
            "hypernetwork_4": (HypernetworkList,),
            "hypernetwork_4_weight": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),

            "use_hypernetwork_5": ("BOOLEAN", {"default": False}),
            "hypernetwork_5": (HypernetworkList,),
            "hypernetwork_5_weight": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),

            "use_hypernetwork_6": ("BOOLEAN", {"default": False}),
            "hypernetwork_6": (HypernetworkList,),
            "hypernetwork_6_weight": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),
        }
    }

    def primere_hypernetwork(self, model, model_version, stack_version = 'Any', safe_load = True, **kwargs):
        model_hypernetwork = model
        if model_version == 'SDXL_2048' and stack_version == 'SD':
            return (model, [],)

        if model_version != 'SDXL_2048' and stack_version == 'SDXL':
            return (model, [],)

        hnetworks = [kwargs.get(f"hypernetwork_{i}") for i in range(1, self.EMBCOUNT + 1)]
        use_hnetworks = [kwargs.get(f"use_hypernetwork_{i}") for i in range(1, self.EMBCOUNT + 1)]
        hnetworks_weight = [kwargs.get(f"hypernetwork_{i}_weight") for i in range(1, self.EMBCOUNT + 1)]

        hnetwork_stack = [(hn_name, hn_weight) for hn_name, hn_weight, hn_uses in zip(hnetworks, hnetworks_weight, use_hnetworks) if hn_uses == True]
        if hnetwork_stack is not None and len(hnetwork_stack) > 0:
            cloned_model = model
            for hn_tuple in hnetwork_stack:
                hypernetwork_path = folder_paths.get_full_path("hypernetworks", hn_tuple[0])
                model_hypernetwork = cloned_model.clone()
                try:
                    patch = hypernetwork.load_hypernetwork_patch(hypernetwork_path, hn_tuple[1], safe_load)
                except Exception:
                    patch = None
                if patch is not None:
                    model_hypernetwork.set_model_attn1_patch(patch)
                    model_hypernetwork.set_model_attn2_patch(patch)
                    cloned_model = model_hypernetwork
        else:
            return (model, [],)

        return (model_hypernetwork, hnetwork_stack,)

class PrimereLYCORIS:
    RETURN_TYPES = ("MODEL", "CLIP", "LYCORIS_STACK", "MODEL_KEYWORD")
    RETURN_NAMES = ("MODEL", "CLIP", "LYCORIS_STACK", "LYCORIS_KEYWORD")
    FUNCTION = "primere_lycoris_stacker"
    CATEGORY = TREE_NETWORKS
    LYCOSCOUNT = 6

    @classmethod
    def INPUT_TYPES(cls):
        LYCO_DIR = os.path.join(comfy_dir, 'models', 'lycoris')
        folder_paths.add_model_folder_path("lycoris", LYCO_DIR)
        LyCORIS = folder_paths.get_filename_list("lycoris")
        LyCORISList = folder_paths.filter_files_extensions(LyCORIS, ['.ckpt', '.safetensors'])

        return {
            "required": {
                "model": ("MODEL",),
                "clip": ("CLIP",),
                "model_version": ("STRING", {"default": 'BaseModel_1024', "forceInput": True}),
                "stack_version": (["SD", "SDXL", "Any"], {"default": "Any"}),
                "use_only_model_weight": ("BOOLEAN", {"default": True}),

                "use_lycoris_1": ("BOOLEAN", {"default": False}),
                "lycoris_1": (LyCORISList,),
                "lycoris_1_model_weight": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),
                "lycoris_1_clip_weight": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),

                "use_lycoris_2": ("BOOLEAN", {"default": False}),
                "lycoris_2": (LyCORISList,),
                "lycoris_2_model_weight": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),
                "lycoris_2_clip_weight": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),

                "use_lycoris_3": ("BOOLEAN", {"default": False}),
                "lycoris_3": (LyCORISList,),
                "lycoris_3_model_weight": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),
                "lycoris_3_clip_weight": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),

                "use_lycoris_4": ("BOOLEAN", {"default": False}),
                "lycoris_4": (LyCORISList,),
                "lycoris_4_model_weight": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),
                "lycoris_4_clip_weight": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),

                "use_lycoris_5": ("BOOLEAN", {"default": False}),
                "lycoris_5": (LyCORISList,),
                "lycoris_5_model_weight": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),
                "lycoris_5_clip_weight": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),

                "use_lycoris_6": ("BOOLEAN", {"default": False}),
                "lycoris_6": (LyCORISList,),
                "lycoris_6_model_weight": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),
                "lycoris_6_clip_weight": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),

                "use_lycoris_keyword": ("BOOLEAN", {"default": False}),
                "lycoris_keyword_placement": (["First", "Last"], {"default": "Last"}),
                "lycoris_keyword_selection": (["Select in order", "Random select"], {"default": "Select in order"}),
                "lycoris_keywords_num": ("INT", {"default": 1, "min": 1, "max": 50, "step": 1}),
                "lycoris_keyword_weight": ("FLOAT", {"default": 1.0, "min": 0, "max": 10.0, "step": 0.1}),
            },
        }

    def primere_lycoris_stacker(self, model, clip, use_only_model_weight, use_lycoris_keyword, lycoris_keyword_placement, lycoris_keyword_selection, lycoris_keywords_num, lycoris_keyword_weight, stack_version = 'Any', model_version = "BaseModel_1024", **kwargs):
        model_keyword = [None, None]

        if model_version == 'SDXL_2048' and stack_version == 'SD':
            return (model, clip, [], model_keyword)

        if model_version != 'SDXL_2048' and stack_version == 'SDXL':
            return (model, clip, [], model_keyword)

        lycoris = [kwargs.get(f"lycoris_{i}") for i in range(1, self.LYCOSCOUNT + 1)]
        model_weight = [kwargs.get(f"lycoris_{i}_model_weight") for i in range(1, self.LYCOSCOUNT + 1)]
        if use_only_model_weight == True:
            clip_weight =[kwargs.get(f"lycoris_{i}_model_weight") for i in range(1, self.LYCOSCOUNT + 1)]
        else:
            clip_weight =[kwargs.get(f"lycoris_{i}_clip_weight") for i in range(1, self.LYCOSCOUNT + 1)]

        uses = [kwargs.get(f"use_lycoris_{i}") for i in range(1, self.LYCOSCOUNT + 1)]
        lycoris_stack = [(lycoris_name, lycoris_model_weight, lycoris_clip_weight) for lycoris_name, lycoris_model_weight, lycoris_clip_weight, lycoris_uses in zip(lycoris, model_weight, clip_weight, uses) if lycoris_uses == True]

        lycoris_params = list()
        if lycoris_stack and len(lycoris_stack) > 0:
            lycoris_params.extend(lycoris_stack)
        else:
            return (model, clip, lycoris_stack, model_keyword)

        model_lyco = model
        clip_lyco = clip
        list_of_keyword_items = []
        lycoris_keywords_num_set = lycoris_keywords_num

        for tup in lycoris_params:
            lycoris_name, strength_model, strength_clip = tup

            lycoris_path = folder_paths.get_full_path("lycoris", lycoris_name)
            lyco = comfy.utils.load_torch_file(lycoris_path, safe_load=True)
            model_lyco, clip_lyco = comfy.sd.load_lora_for_models(model_lyco, clip_lyco, lyco, strength_model, strength_clip)

            lyconame_only = Path(lycoris_name).stem
            model_lyco_version = utility.get_value_from_cache('lycoris_version', lyconame_only)
            if model_lyco_version is None:
                lycoVER = utility.getLoraVersion(lyco)
                if lycoVER is not None:
                    utility.add_value_to_cache('lycoris_version', lyconame_only, lycoVER)

            if use_lycoris_keyword == True:
                ModelKvHash = utility.get_model_hash(lycoris_path)
                if ModelKvHash is not None:
                    KEYWORD_PATH = os.path.join(PRIMERE_ROOT, 'front_end', 'keywords', 'lora-keyword.txt')
                    keywords = utility.get_model_keywords(KEYWORD_PATH, ModelKvHash, lycoris_name)
                    if keywords is not None and keywords != "" and isinstance(keywords, str) == True:
                        if keywords.find('|') > 1:
                            keyword_list = [word.strip() for word in keywords.split('|')]
                            keyword_list = list(filter(None, keyword_list))
                            if (len(keyword_list) > 0):
                                lycoris_keywords_num = lycoris_keywords_num_set
                                keyword_qty = len(keyword_list)
                                if (lycoris_keywords_num > keyword_qty):
                                    lycoris_keywords_num = keyword_qty
                                if lycoris_keyword_selection == 'Select in order':
                                    list_of_keyword_items.extend(keyword_list[:lycoris_keywords_num])
                                else:
                                    list_of_keyword_items.extend(random.sample(keyword_list, lycoris_keywords_num))
                        else:
                            list_of_keyword_items.append(keywords)

        if len(list_of_keyword_items) > 0:
            if lycoris_keyword_selection != 'Select in order':
                random.shuffle(list_of_keyword_items)

            list_of_keyword_items = list(set(list_of_keyword_items))
            keywords = ", ".join(list_of_keyword_items)

            if (lycoris_keyword_weight != 1):
                keywords = '(' + keywords + ':' + str(round(lycoris_keyword_weight, 1)) + ')'

            model_keyword = [keywords, lycoris_keyword_placement]

        return (model_lyco, clip_lyco, lycoris_stack, model_keyword)