import os
from .my_smart_load_image import MySmartLoadImage
from .my_turbo_color_fix import MyTurboColorFix
from .h3_static_camera import MyH3StaticCamera

# Автоматически определяем, где лежит папка с нодой, чтобы читать системный промпт напрямую из репозитория
NODE_ROOT = os.path.dirname(os.path.abspath(__file__))
PROMPT_PATH = os.path.join(NODE_ROOT, "prompts", "H3_NSFW_Engine 1.txt")

NODE_CLASS_MAPPINGS = {
    "SmartLoadAndResizeImage": MySmartLoadImage,
    "TurboColorFixAdaIN": MyTurboColorFix,
    "FixedCameraH3Presets": MyH3StaticCamera
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SmartLoadAndResizeImage": "⚡ Smart Load & Resize Image",
    "TurboColorFixAdaIN": "⚡ Manual Color & Upscale Panel",
    "FixedCameraH3Presets": "⚡ Fixed Camera H3 (Presets)"
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS', 'PROMPT_PATH']
