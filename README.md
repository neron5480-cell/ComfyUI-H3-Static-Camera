# ⚡ ComfyUI-H3-Static-Camera & Video Toolset

### English
Lightweight custom nodes + LLM engine for ComfyUI, built specifically for high-quality video generation with MiniMax-H3.  
Removes node spaghetti, prevents OOM errors even on 8 GB VRAM, and provides professional color correction.  
Written in pure Python/PyTorch with zero heavy third-party dependencies.

### Русский
Лёгкий набор авторских нод и LLM-движок для ComfyUI, созданный специально под генерацию видео на MiniMax-H3.  
Убирает «паутину» из нод, защищает от OOM даже на 8 ГБ VRAM и даёт профессиональную цветокоррекцию.  
Код написан на чистом ядре без тяжёлых сторонних зависимостей.

---

## 🧠 LLM Core Engine / Системный промптер

### `prompts/H3_NSFW_Engine 1.txt`

#### English
Core system prompt tuned for Qwen 3.5 9B (works with any autoprompter node).

**Key features:**
- Camera is strictly locked by default (no zoom, no movement)
- Allows camera changes only if explicitly requested in the user prompt
- Lets you write simple 1–2 line prompts without following strict MiniMax-H3 syntax
- Specifically designed to work with the **Fixed Camera H3 (Presets)** node (leaves hidden technical markers)
- Full support for adult content with zero censorship

**Important:**  
In the `LLM Text Processor` node you **must** manually select `H3_NSFW_Engine 1.txt` in the `system_prompt` field.

#### Русский
Основное ядро системного промпта под Qwen 3.5 9B (можно использовать с любой нодой автопромптера).

**Ключевые особенности:**
- По умолчанию камера жёстко заблокирована (нет зума и движений)
- Изменение камеры разрешается только если это прямо указано в промпте пользователя
- Можно писать простые промпты в 1–2 строки без соблюдения сложных правил разметки MiniMax-H3
- Специально написан для работы с нодой **Fixed Camera H3 (Presets)** (оставляет технические маркеры)
- Полная поддержка взрослого контента без цензуры

**Важно:**  
В ноде `LLM Text Processor` обязательно выберите файл `H3_NSFW_Engine 1.txt` в поле `system_prompt`.

---

## 🛠️ Included Nodes / Что входит в набор

### 1. Smart Load & Resize Image

#### English
Prepares any image for video generation in one step.  
Supports presets, aspect ratios, megapixel targeting and hard `divisible_by = 32` rounding to completely prevent VAE crashes.  
“Disabled” mode crops edges pixel-perfect without changing object scale.

#### Русский
Готовит любое изображение к генерации видео за один шаг.  
Поддерживает пресеты, соотношения сторон, мегапиксели и жёсткое округление до кратности 32 (полная защита от вылетов VAE).  
Режим “Disabled” подрезает края пиксель-в-пиксель без изменения масштаба объектов.

### 2. Fixed Camera H3 (Presets)

#### English
Director-style camera control for MiniMax-H3.

- **Automatic mode** — tightly linked to the `H3_NSFW_Engine 1` prompt. The node scans and carefully modifies only the technical markers without touching the artistic text.
- **Manual mode** — works independently. Forces exact camera coordinates onto any English prompt.

#### Русский
Режиссёрский пульт управления камерой для MiniMax-H3.

- **Автоматический режим** — жёстко привязан к структуре промпта от `H3_NSFW_Engine 1`. Нода аккуратно меняет только технические маркеры, не трогая художественный текст.
- **Ручной режим** — работает автономно. Принудительно вшивает точные координаты камеры в любой английский промпт.

### 3. Manual Color & Upscale Panel

#### English
All-in-one panel that fixes AI color drift and over-exposure (“deep-frying”) on low-step Turbo modes.  
Includes fast tensor-based Unsharp Masking, color/contrast controls and a reliable upscale pipeline with error fallbacks.  
Can be used anywhere in the workflow (including preprocessing the source image).

#### Русский
Универсальный пульт «всё в одном» для исправления ИИ-пережаривания цветов на малых шагах (Turbo-режимы).  
Включает быстрый фильтр резкости на тензорах, управление яркостью/контрастом и надёжный апскейл с защитой от падений.  
Можно использовать в любом месте workflow (в том числе для предобработки референса).

---

## 🚀 Key Advantages / Главные плюсы

#### English
- **VRAM-friendly (8 GB+)** — stable work even on budget cards  
- **Zero bloat** — pure Python/PyTorch, doesn’t break on ComfyUI updates  
- **Anti-spaghetti** — replaces chains of 5–10 regular nodes with one clean block

#### Русский
- **Дружелюбен к VRAM (от 8 ГБ)** — стабильная работа даже на бюджетных картах  
- **Без лишнего** — чистый Python/PyTorch, не ломается при обновлениях ComfyUI  
- **Анти-паутина** — заменяет цепочки из 5–10 обычных нод одним удобным блоком

---

*Developed by **neron5408922***
