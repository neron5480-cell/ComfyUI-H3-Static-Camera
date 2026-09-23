import torch
import torch.nn.functional as F

class MyTurboColorFix:
    def __init__(self):
        pass
        
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "BRIGHTNESS / ЯРКОСТЬ": ("FLOAT", {"default": 0.0, "min": -0.50, "max": 0.50, "step": 0.01, "display": "slider"}),
                "CONTRAST / КОНТРАСТ": ("FLOAT", {"default": 1.0, "min": 0.50, "max": 1.80, "step": 0.01, "display": "slider"}),
                "SATURATION / НАСЫЩЕННОСТЬ": ("FLOAT", {"default": 1.0, "min": 0.00, "max": 1.80, "step": 0.01, "display": "slider"}),
                "SHARPNESS / РЕЗКОСТЬ": ("FLOAT", {"default": 0.0, "min": 0.00, "max": 2.00, "step": 0.05, "display": "slider"}),
                # Кнопка включения и выключения апскейла на два языка
                "upscale": (["Disabled / Откл", "Enabled / Вкл"], {"default": "Disabled / Откл"}),
                "upscale_scale": ("FLOAT", {"default": 2.00, "min": 1.00, "max": 4.00, "step": 0.25}),
            },
            "optional": {
                "upscale_model": ("UPSCALE_MODEL",),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "apply_manual_color"
    CATEGORY = "AIVideoPostprocessing"

    def apply_manual_color(self, image, **kwargs):
        # Вытаскиваем значения по новым именам аргументов
        brightness_val = kwargs.get("BRIGHTNESS / ЯРКОСТЬ", 0.0)
        contrast_val = kwargs.get("CONTRAST / КОНТРАСТ", 1.0)
        saturation_val = kwargs.get("SATURATION / НАСЫЩЕННОСТЬ", 1.0)
        sharpness_val = kwargs.get("SHARPNESS / РЕЗКОСТЬ", 0.0)
        upscale = kwargs.get("upscale", "Disabled / Откл")
        upscale_scale = kwargs.get("upscale_scale", 2.00)
        upscale_model = kwargs.get("upscale_model", None)

        device = image.device
        dtype = image.dtype
        
        # Переводим в формат [B, C, H, W]
        frames = image.permute(0, 3, 1, 2).clone()
        
        # 1. КОРРЕКЦИЯ ЯРКОСТИ
        if brightness_val != 0.0:
            frames = frames + brightness_val
            
        # 2. КОРРЕКЦИЯ КОНТРАСТА
        if contrast_val != 1.0:
            mean_val = torch.mean(frames, dim=(2, 3), keepdim=True)
            frames = (frames - mean_val) * contrast_val + mean_val
            
        # 3. КОРРЕКЦИЯ НАСЫЩЕННОСТИ
        if saturation_val != 1.0:
            grayscale = frames[:, 0:1, :, :] * 0.299 + frames[:, 1:2, :, :] * 0.587 + frames[:, 2:3, :, :] * 0.114
            frames = grayscale + (frames - grayscale) * saturation_val
            
        # 4. ДОБАВЛЕНИЕ РЕЗКОСТИ (Unsharp Masking на тензорах)
        if sharpness_val > 0.0:
            kernel = torch.tensor([[1/9, 1/9, 1/9], [1/9, 1/9, 1/9], [1/9, 1/9, 1/9]], dtype=dtype, device=device)
            kernel = kernel / kernel.sum()
            kernel = kernel.view(1, 1, 3, 3).repeat(3, 1, 1, 1)
            
            blurred = F.conv2d(frames, kernel, padding=1, groups=3)
            frames = frames + (frames - blurred) * sharpness_val

        # Зажимаем цвета в диапазон [0.0, 1.0] и возвращаем в стандартный [B, H, W, C]
        frames = torch.clamp(frames, 0.0, 1.0)
        final_output = frames.permute(0, 2, 3, 1)
        
        # 5. БЛОК ИИ-АПСКЕЙЛА
        if "Enabled" in upscale and upscale_model is not None:
            try:
                batch, orig_h, orig_w, channels = final_output.shape
                target_w = int(orig_w * upscale_scale)
                target_h = int(orig_h * upscale_scale)
                
                if hasattr(upscale_model, "model"):
                    model_to_run = upscale_model.model
                else:
                    model_to_run = upscale_model
                
                model_device = getattr(model_to_run, "device", device)
                input_tensor = final_output.permute(0, 3, 1, 2).to(model_device)
                
                with torch.inference_mode():
                    if hasattr(upscale_model, "upscale"):
                        upscaled = upscale_model.upscale(final_output)
                    else:
                        if hasattr(model_to_run, "predict"):
                            upscaled = model_to_run.predict(input_tensor)
                        elif hasattr(model_to_run, "forward"):
                            upscaled = model_to_run.forward(input_tensor)
                        else:
                            upscaled = model_to_run(input_tensor)
                        upscaled = upscaled.permute(0, 2, 3, 1)
                
                upscaled = upscaled.to(device)
                
                # ЮВЕЛИРНАЯ ПРОВЕРКА КРАТНОСТИ ФОРМЫ
                if upscaled.shape[1] != target_h or upscaled.shape[2] != target_w:
                    upscaled_p = upscaled.permute(0, 3, 1, 2)
                    upscaled_res = torch.nn.functional.interpolate(
                        upscaled_p, size=(target_h, target_w), mode="bilinear", align_corners=False
                    )
                    upscaled = upscaled_res.permute(0, 2, 3, 1)
                    
                final_output = torch.clamp(upscaled, 0.0, 1.0)
                
            except Exception as e:
                print(f"[⚡ Turbo Color Fix] Upscale error, applied standard resize fallback: {str(e)}")
                batch, orig_h, orig_w, channels = final_output.shape
                target_w = int(orig_w * upscale_scale)
                target_h = int(orig_h * upscale_scale)
                
                upscaled_fallback = final_output.permute(0, 3, 1, 2)
                upscaled_fallback = torch.nn.functional.interpolate(
                    upscaled_fallback, size=(target_h, target_w), mode="bilinear", align_corners=False
                )
                final_output = upscaled_fallback.permute(0, 2, 3, 1)
        
        return (final_output,)

NODE_CLASS_MAPPINGS = {
    "TurboColorFixAdaIN": MyTurboColorFix
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TurboColorFixAdaIN": "⚡ Manual Color & Upscale Panel"
}
