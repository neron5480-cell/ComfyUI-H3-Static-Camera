from .my_smart_load_image import MySmartLoadImage
from .my_turbo_color_fix import MyTurboColorFix
from .h3_static_camera import MyH3StaticCamera

NODE_CLASS_MAPPINGS = {
    "SmartLoadAndResizeImage": MySmartLoadImage,
    "TurboColorFixAdaIN": MyTurboColorFix,
    "FixedCameraH3Presets": MyH3StaticCamera
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SmartLoadAndResizeImage": "⚡ Smart Load & Resize Image",
    "TurboColorFixAdaIN": "⚡ Ручной Пульт Цвета & Апскейл",
    "FixedCameraH3Presets": "⚡ Fixed Camera H3 (Presets)"
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
