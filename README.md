# ⚡ ComfyUI-H3-Static-Camera & Video Toolset

[EN] A powerful, lightweight custom node set and LLM engine built specifically for ComfyUI to streamline high-end video generation (MiniMax-H3 ), eliminate "node spaghetti," prevent Out-Of-Memory (OOM) errors on 8GB VRAM cards, and provide professional color correction. Built entirely on pure core logic without heavy third-party dependencies.

[RU] Мощный и легкий набор авторских нод и LLM-движок для ComfyUI. Создан для оптимизации генерации видео (модели MiniMax-H3 ), полной ликвидации "паутины из макарон", защиты от вылетов по памяти (OOM) на видеокартах от 8 ГБ VRAM и профессиональной (цветокоррекции). Код написан на чистом ядре без тяжелых сторонних зависимостей.

---

## 📊 Required Models / Необходимые модели

[RU] **Скачайте эти модели (с Civitai / HuggingFace) и разложите их строго по указанным папкам:**
1. Основная модель (Diffusion): `minimax_h3_fl2va_pruned_int8_convrot.safetensors` ➔ `ComfyUI/models/unet/`
2. Ускоряющая LoRA (Turbo): `minimax_h3_fl2v_turbo_8step_v1.0_768p_comfyui_bf16.safetensors` ➔ `ComfyUI/models/loras/`
3. Модель внимания (Vision/mmproj): `mmproj-F16.gguf` ➔ `ComfyUI/models/mmproj/`
4. Аудио VAE: `minimax_h3_audio_vae_fp32.safetensors` ➔ `ComfyUI/models/vae/`
5. Видео VAE: `minimax_h3_video_vae_fp16.safetensors` ➔ `ComfyUI/models/vae/`
6. Модель CLIP: `qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors` ➔ `ComfyUI/models/clip/`

[EN] **Download these models (from Civitai / HuggingFace) and place them strictly into the following directories:**
1. Base Model (Diffusion): `minimax_h3_fl2va_pruned_int8_convrot.safetensors` ➔ `ComfyUI/models/unet/`
2. Turbo LoRA: `minimax_h3_fl2v_turbo_8step_v1.0_768p_comfyui_bf16.safetensors` ➔ `ComfyUI/models/loras/`
3. Vision Model (mmproj): `mmproj-F16.gguf` ➔ `ComfyUI/models/mmproj/`
4. Audio VAE: `minimax_h3_audio_vae_fp32.safetensors` ➔ `ComfyUI/models/vae/`
5. Video VAE: `minimax_h3_video_vae_fp16.safetensors` ➔ `ComfyUI/models/vae/`
6. CLIP Model: `qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors` ➔ `ComfyUI/models/clip/`

---

## 🧠 LLM Core Engine / Системный промптер

### ⚡ prompts/H3_NSFW_Engine 1.txt
* **EN:** The core system prompt tuned for Qwen 3.5 9B (can be used as a system prompt in any autoprompter node setup). 
  ⚠️ **Key Features:** By default, the camera is strictly locked (no zoom, no movement). However, it dynamically allows camera changes if explicitly requested in the user's prompt. If no camera instructions are given, the locked state remains absolute. It allows the user to write simple prompts in just 1-2 lines without following strict MiniMax-H3 formatting rules. This prompt is engineered specifically to pair with the **Fixed Camera H3 (Presets)** node, as it generates precision hidden layout markers for the node to intercept. Includes high-fidelity adult content formatting (zero censorship).
  👉 **Note:** Inside your `LLM Text Processor` node, you absolutely must click the `system_prompt` field and manually select `H3_NSFW_Engine 1.txt` from the dropdown list.
* **RU:** Основное ядро системного промпта, прописанное под Qwen 3.5 9B (можно подключать как системный промпт в любую ноду автопромптера).
  ⚠️ **Ключевые фишки:** По умолчанию камера намертво заблокирована (нет зума и движений). Однако движок допускает изменение положения камеры, если это прямо прописано в тексте пользователя. Позволяет писать промпты всего в 1-2 строки, при этом соблюдать сложные правила разметки MiniMax-H3 не обязательно. Этот промпт написан специально для совместной работы с нодой **Fixed Camera H3 (Presets)**, так как оставляет в тексте особые технические маркеры для её точной работы. Включает полную поддержку взрослого контента без цензуры.
  👉 **Важно:** В ноде текстового процессора (`LLM Text Processor`) вам обязательно нужно кликнуть на поле `system_prompt` и выбрать из списка файл `H3_NSFW_Engine 1.txt`.

---

## 🛠️ Included Nodes / Что входит в набор

### 1. ⚡ Smart Load & Resize Image
* **EN:** Automatically prepares any input image for AI video generation in a single step. Features standard presets, aspect ratio lock, megapixel target scaling, and **divisible_by = 32 rounding** to completely eliminate VAE decoder crashes. The "Disabled" mode crops edges pixel-to-pixel without altering object scale.
* **RU:** В одно действие готовит любую картинку к генерации видео. Поддерживает готовые пресеты, соотношения сторон, мегапиксели и **жесткое округление сторон до кратности 32**, что полностью защищает от ошибок VAE. В режиме "Disabled" ювелирно подрезает края пиксель-в-пиксель без изменения масштаба объектов.

### 2. ⚡ Fixed Camera H3 (Presets)
* **EN:** A director's control room for MiniMax-H3 camera movements with advanced routing logic.
  ⚠️ **Core Logic:** In **Automatic Mode**, the camera adjustment is strictly tied to the `H3_NSFW_Engine 1` prompt layout. The node intelligently scans and modifies the technical brief structure without breaking the artistic prompt. In **Manual Mode**, it operates independently, forcing exact technical camera coordinates onto any direct English text input.
* **RU:** Режиссерский пульт управления камерой для MiniMax-H3 с продвинутой логикой маршрутизации.
  ⚠️ **Важная особенность:** В **Автоматическом режиме** регулировка положения камеры жестко привязана к структуре брифа от `H3_NSFW_Engine 1`. Нода сканирует этот текст и аккуратно модифицирует технические маркеры, не ломая художественный текст. В **Ручном режиме** действует независимо и принудительно вшивает точные координаты камеры в любой английский текст.

### 3. ⚡ Manual Color & Upscale Panel
* **EN:** A lightweight, all-in-one panel designed to rescue animations from AI color drift and over-exposure ("deep-frying") on low step counts (Turbo modes). Includes high-performance, tensor-based Unsharp Masking for edge sharpness, color/contrast grading, and a bulletproof built-in upscale pipeline with automatic error fallbacks. Can be used anywhere in the workflow (including preprocessing source images).
* **RU:** Легкий пульт "все в одном" для спасения видео от ИИ-пережаривания на малых шагах (режимы Турбо). Включает быстрый ИИ-апскейлер с защитой от падения очереди и высокопроизводительный фильтр резкости контуров на тензорах. Абсолютно универсален — можно крутить яркость, контраст и резкость как на выходе, так и для референса на самом старте.

---

## 🚀 Key Advantages / Главные плюсы

* **VRAM Friendly (8 GB+):** Tailored for budget setups to ensure stable, cinematic rendering without memory leaks.
* **Zero Bloat:** Pure core Python/PyTorch logic. Won't break or crash during official ComfyUI updates.
* **Anti-Spaghetti:** Replaces complex chains of 5-10 native nodes with elegant, multi-functional blocks.

---
*Developed with dedication by **neron5408922**.*
