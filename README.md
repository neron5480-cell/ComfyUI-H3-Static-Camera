# ⚡ ComfyUI-H3-Static-Camera & Video Toolset

[EN] A powerful, lightweight custom node set built specifically for ComfyUI to streamline high-end video generation (MiniMax-H3 / LTX models), eliminate "node spaghetti," prevent Out-Of-Memory (OOM) errors on 8GB VRAM cards, and provide professional color correction. Built entirely on pure core logic without heavy third-party dependencies.

[RU] Мощный и легкий набор авторских нод для ComfyUI. Создан для оптимизации генерации видео (модели MiniMax-H3 / LTX), полной ликвидации "паутины из макарон", защиты от вылетов по памяти (OOM) на видеокартах от 8 ГБ VRAM и профессиональной цветокоррекции. Код написан на чистом ядре без тяжелых сторонних зависимостей.

---

## 🛠️ Included Nodes / Что входит в набор

### 1. ⚡ Smart Load & Resize Image
* **EN:** Automatically prepares any input image for AI video generation in a single step. Features standard presets, aspect ratio lock, megapixel target scaling, and **divisible_by = 32 rounding** to completely eliminate VAE decoder crashes. The "Disabled" mode crops edges pixel-to-pixel without altering object scale.
* **RU:** В одно действие готовит любую картинку к генерации видео. Поддерживает готовые пресеты, соотношения сторон, мегапиксели и **жесткое округление сторон до кратности 32**, что полностью защищает от ошибок VAE. В режиме "Disabled" ювелирно подрезает края пиксель-в-пиксель без изменения масштаба объектов.

### 2. ⚡ Fixed Camera H3 (Presets)
* **EN:** A director's control room for MiniMax-H3 camera movements. In **LLM Autoprompter mode**, it seamlessly injects technical camera vectors and framing constraints into the AI text brief without breaking the artistic prompt. Supports both Russian and English user inputs.
* **RU:** Режиссерский пульт управления камерой для MiniMax-H3. В режиме **Автопромптера** аккуратно вшивает технические маркеры ракурса в ИИ-бриф, вообще не ломая художественный текст. Позволяет писать промпты как на английском, так и на русском языке.

### 3. ⚡ Manual Color & Upscale Panel
* **EN:** A lightweight, all-in-one panel designed to rescue animations from AI over-exposure ("deep-frying") on low step counts (Turbo modes). Includes high-performance, tensor-based Unsharp Masking for edge sharpness, color/contrast grading, and a bulletproof built-in upscale pipeline with automatic error fallbacks. Can be used anywhere in the workflow (including preprocessing source images).
* **RU:** Легкий пульт "все в одном" для спасения видео от ИИ-пережаривания на малых шагах (режимы Турбо). Включает быстрый ИИ-апскейлер с защитой от падения очереди и высокопроизводительный фильтр резкости контуров на тензорах. Абсолютно универсален — можно крутить яркость, контраст и резкость как на выходе, так и для референса на самом старте.

---

## 🚀 Key Advantages / Главные плюсы

* **VRAM Friendly (8 GB+):** Tailored for budget setups to ensure stable, cinematic rendering without memory leaks.
* **Zero Bloat:** Pure core Python/PyTorch logic. Won't break or crash during official ComfyUI updates.
* **Anti-Spaghetti:** Replaces complex chains of 5-10 native nodes with elegant, multi-functional blocks.

---
*Developed with dedication by **neron5408922**.*
