import json
import re

class MyH3StaticCamera:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                # НАШ НОВЫЙ ТУМБЛЕР РЕЖИМА ВСЕГО ВОРКФЛУ
                "workflow_mode": ([
                    "[LLM] Автопромтер (Бриф Naxdy)", 
                    "[Manual] Обычный текст (Прямой ввод)"
                ], {"default": "[LLM] Автопромтер (Бриф Naxdy)"}),
                
                "camera_mode": ([
                    "АВТО (Слушать автопромтер)",
                    "ФРОНТ (Прямой ракурс)", 
                    "СЛЕВА (Боковой ракурс)", 
                    "СПРАВА (Боковой ракурс)", 
                    "СЗАДИ (Со спины)", 
                    "СВЕРХУ (Высокий угол)", 
                    "СНИЗУ (Низкий угол)"
                ], {"default": "АВТО (Слушать автопромтер)"}),
                "framing_type": (["wide shot", "medium shot", "close-up"], {"default": "medium shot"}),
                "total_frames": ("INT", {"default": 124, "min": 1, "max": 1000, "step": 1}),
                "fps": ("INT", {"default": 24, "min": 1, "max": 60, "step": 1}),
                "fixed_distance": ("FLOAT", {"default": 1.00, "min": 0.10, "max": 3.00, "step": 0.05}),
            },
            "optional": {
                "autoprompt_text": ("STRING", {"forceInput": True}),  # Сюда идет выход из Qwen
                "manual_prompt": ("STRING", {"default": "", "multiline": True}),  # НАШ НОВЫЙ ВХОД ДЛЯ ОБЫЧНОГО ТЕКСТА
                "subject_details": ("STRING", {"default": "", "multiline": True}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING", "INT")
    RETURN_NAMES = ("minimax_prompt", "storyboard_json", "h3world_actions", "frames_count")
    FUNCTION = "generate_static_data"
    CATEGORY = "AIVideoPostprocessing"

    def generate_static_data(self, workflow_mode, camera_mode, framing_type, total_frames, fps, fixed_distance, autoprompt_text="", manual_prompt="", subject_details=""):
        safe_fps = max(1, fps)
        duration = round(total_frames / safe_fps, 2)
        
        azimuth_val = 0.0
        elevation_val = 0.0
        zone_name = "Front"
        camera_text_desc = "completely locked-off camera remains fixed in a front view"
        summary_camera_addon = "while the camera stays completely locked in a front view."

        # АВТООПРЕДЕЛЕНИЕ: Какой текст анализировать на ключевые слова углов
        if workflow_mode == "[LLM] Автопромтер (Бриф Naxdy)":
            incoming_text = str(autoprompt_text)
        else:
            incoming_text = str(manual_prompt)
            
        text_to_analyze = (incoming_text + " " + str(subject_details)).lower()
        is_auto = (camera_mode == "АВТО (Слушать автопромтер)")
        
        # 1. СКАНИРОВАНИЕ ТЕКСТА НА ПРЕДМЕТ ВЕКТОРОВ И НАПРАВЛЕНИЙ
        if is_auto:
            if any(x in text_to_analyze for x in ["слева", "left side", "left view"]):
                camera_mode_resolved = "СЛЕВА"
            elif any(x in text_to_analyze for x in ["справа", "right side", "right view"]):
                camera_mode_resolved = "СПРАВА"
            elif any(x in text_to_analyze for x in ["сзади", "behind", "back view"]):
                camera_mode_resolved = "СЗАДИ"
            elif any(x in text_to_analyze for x in ["сверху", "high angle", "top view", "high-angle"]):
                camera_mode_resolved = "СВЕРХУ"
            elif any(x in text_to_analyze for x in ["снизу", "low angle", "bottom view"]):
                camera_mode_resolved = "СНИЗУ"
            else:
                camera_mode_resolved = "ФРОНТ"
        else:
            camera_mode_resolved = camera_mode

        # 2. МАТЕМАТИКА 3D УГЛОВ И СИНТАКСИС ДЛЯ КОРРЕКЦИИ ТЕКСТА
        if "СЛЕВА" in camera_mode_resolved:
            azimuth_val = -90.0
            zone_name = "Left"
            camera_text_desc = "static camera positioned strictly on the LEFT side, showing a side view"
            summary_camera_addon = "while the camera stays completely locked in a left side view."
        elif "СПРАВА" in camera_mode_resolved:
            azimuth_val = 90.0
            zone_name = "Right"
            camera_text_desc = "static camera positioned strictly on the RIGHT side, showing a side view"
            summary_camera_addon = "while the camera stays completely locked in a right side view."
        elif "СЗАДИ" in camera_mode_resolved:
            azimuth_val = 180.0
            zone_name = "Behind"
            camera_text_desc = "static camera positioned strictly BEHIND the subject, showing a back view"
            summary_camera_addon = "while the camera stays completely locked in a back view."
        elif "СВЕРХУ" in camera_mode_resolved:
            elevation_val = 45.0
            zone_name = "Top (High Angle)"
            camera_text_desc = "static camera positioned at a HIGH ANGLE, looking down from above"
            summary_camera_addon = "while the camera stays completely locked in a high angle top view."
        elif "СНИЗУ" in camera_mode_resolved:
            elevation_val = -30.0
            zone_name = "Bottom (Low Angle)"
            camera_text_desc = "static camera positioned at a LOW ANGLE, looking up from below"
            summary_camera_addon = "while the camera stays completely locked in a low angle bottom view."
        else:
            azimuth_val = 0.0
            elevation_val = 0.0
            zone_name = "Front"
            camera_text_desc = "completely locked-off camera remains fixed in a front view"
            summary_camera_addon = "while the camera stays completely locked in a front view."

        # Базовая жесткая инструкция камеры для MiniMax (Идет на самый верх)
        base_prompt = f"[CAMERA] [Static shot] A {camera_text_desc}. "
        base_prompt += f"The framing is a rigid {framing_type} at distance {fixed_distance}. Absolutely no zoom, no camera parallax, no dolly, and no tracking. "
        base_prompt += "All background elements and furniture are anchored and perfectly rigid."

        # 3. СБОРКА И МОДИФИКАЦИЯ ТЕКСТА В ЗАВИСИМОСТИ ОТ ВЫБРАННОГО РЕЖИМА ВОРКФЛУ
        if workflow_mode == "[LLM] Автопромтер (Бриф Naxdy)":
            # --- РЕЖИМ 1: РАБОТА С ЯЗЫКОВЫМИ МОДЕЛЯМИ ---
            orig_text = incoming_text.strip()
            if is_auto:
                full_prompt = orig_text if orig_text else f"{base_prompt}"
            else:
                if orig_text:
                    cleaned = re.sub(r'[,.]?\s*while\s+the\s+camera\s+stays\s+[^.\n]+', '', orig_text, flags=re.IGNORECASE)
                    cleaned = re.sub(r'[,.]?\s*and\s+the\s+camera\s+stays\s+[^.\n]+', '', cleaned, flags=re.IGNORECASE)
                    cleaned = re.sub(r'[,.]?\s*the\s+camera\s+remains\s+[^.\n]+', '', cleaned, flags=re.IGNORECASE)
                    cleaned = re.sub(r'[,.]?\s*camera\s+remains\s+[^.\n]+', '', cleaned, flags=re.IGNORECASE)
                    cleaned = re.sub(r'\[camera\][^.\n]+', '', cleaned, flags=re.IGNORECASE)
                    
                    lines = cleaned.split('\n')
                    for i, line in enumerate(lines):
                        if line.strip().lower().startswith("summary:"):
                            pure_line = line.strip().rstrip('.')
                            lines[i] = f"{pure_line}, {summary_camera_addon}"
                            break
                    full_prompt = f"{base_prompt}\n\n{'\n'.join(lines)}"
                else:
                    full_prompt = base_prompt
        else:
            # --- РЕЖИМ 2: ОВЕРКЛОК ПОД ОБЫЧНЫЙ ТЕКСТ (РУЧНОЙ ВВОД ПОЛЬЗОВАТЕЛЯ) ---
            user_text = incoming_text.strip()
            
            # Нода сама оборачивает простой текст пользователя в правильные блоки MiniMax-H3!
            built_prompt = f"{base_prompt}\n\n"
            built_prompt += f"summary: [keyframe completion] {user_text if user_text else 'A scene unfolds'}, {summary_camera_addon}\n"
            
            if subject_details and subject_details.strip():
                built_prompt += f"subject_definitions: {subject_details.strip()}\n"
                
            full_prompt = built_prompt

        # 4. ГЕНЕРАЦИЯ СТРУКТУРЫ JSON (Ваша идеальная математика координат)
        storyboard = {
            "schema": "h3-camera-plan-v1",
            "camera_choreography": f"CAMERA LOCKED AT {zone_name.upper()} POSITION.",
            "total_orbit_travel_degrees": 0.0,
            "net_orbit_travel_degrees": 0.0,
            "camera_speed": "constant",
            "duration": duration,
            "fps": float(safe_fps),
            "segments": [
                {
                    "id": "frozen_automatic_anchor",
                    "start": 0.0,
                    "end": duration,
                    "camera_travel": "none",
                    "signed_orbit_degrees": 0.0,
                    "interpolation": "linear",
                    "start_pose": {"azimuth": azimuth_val, "elevation": elevation_val, "distance": fixed_distance},
                    "end_pose": {"azimuth": azimuth_val, "elevation": elevation_val, "distance": fixed_distance}
                }
            ],
            "final": f"Freeze composition until {duration}s."
        }

        legacy_actions = [
            {"time": 0.0, "azimuth": azimuth_val, "elevation": elevation_val, "distance": fixed_distance},
            {"time": duration, "azimuth": azimuth_val, "elevation": elevation_val, "distance": fixed_distance}
        ]

        return (full_prompt, json.dumps(storyboard, indent=2), json.dumps(legacy_actions), total_frames)

NODE_CLASS_MAPPINGS = {
    "FixedCameraH3Presets": MyH3StaticCamera
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "FixedCameraH3Presets": "⚡ Fixed Camera H3 (Presets)"
}
