# 侘寂 × 北歐質感美學 Z-Image LoRA 研究

## 研究結論

目前 Z-Image (z-image.me) 平台的 ZIT LoRA 庫中，**沒有專門針對「侘寂北歐質感美學」(Japandi) 風格的現成 LoRA**。Z-Image 的 LoRA 庫以角色、寫實、動漫風格為主。

以下整理了替代方案與相關資源。

---

## 方案一：Z-Image i2L 自行訓練（推薦）

Z-Image i2L 是阿里巴巴通義實驗室 2026 年 1 月發布的 Image-to-LoRA 工具：

- 只需 **一張參考圖片** 即可在 10 秒內生成 LoRA
- 支援 PyTorch 框架，最低 16GB VRAM 即可運行
- 建議參數：`cfg_scale=4`, `sigma_shift=8`
- 官方連結：https://z-image.me/en/blog/z-image-i2l-released

**做法**：找一張理想的侘寂北歐風格 (Japandi) 參考圖，用 i2L 生成專屬 LoRA。

---

## 方案二：Civitai 上相關 LoRA

Z-Image Turbo 支援標準 `.safetensors` 格式，與 SDXL 系列高度相容。以下為最相關的 LoRA：

### 1. Interior-Design-Universal SDXL（最推薦）

- **連結**：https://civitai.com/models/496075/interior-design-universal-sdxl
- **說明**：支援多種室內風格，包含 wabi-sabi 與 Nordic
- **觸發詞**：
  - 侘寂風：`wabi-sabi style` / `wabi-sabi_style` / `wabi-sabi elements`
  - 北歐風：`Nordic style` / `Nordic_style` / `Nordic elements`
- **建議**：同時使用 `wabi-sabi_style, Nordic elements` 融合兩種風格
- **注意**：SDXL 模型建議開啟 refiner，取樣值設定 20-25

### 2. XSarchitectural-8japanwabisabi

- **連結**：https://civitai.com/models/25384/xsarchitectural-8japanwabisabi
- **說明**：專注日式侘寂室內設計風格
- **格式**：SD 1.5 LoRA (.safetensors, 36.11 MB)
- **注意**：建議搭配 CKPT + VAE 使用

### 3. XSarchitectural-9 Japanese wabi-sabi (進階版)

- **連結**：https://civitai.com/models/25447/xsarchitectural-9advanced-interior-design-based-on-japanese-style
- **說明**：進階日式侘寂室內設計，搭配 ControlNet 效果更佳

### 4. Wabi-sabi Style Restaurant

- **連結**：https://civitai.com/models/119656/wabi-sabi-style-restaurant
- **說明**：侘寂風餐廳設計，以工業風裝飾為主，也可用於居家
- **格式**：SD 1.5 LoRA

### 5. Nordic Luxury Interior Design 1.0

- **連結**：https://civitai.com/models/124091/nordic-luxury-interior-design-10
- **說明**：北歐奢華極簡室內設計風格

---

## 方案三：LoRA 疊加策略

Z-Image Turbo 支援同時疊加最多 **3 個 LoRA**（權重 0.0-4.0）。

建議組合：
1. **Interior-Design-Universal SDXL** (權重 0.7) — 提供室內設計基底
2. **XSarchitectural-8japanwabisabi** (權重 0.5) — 強化侘寂質感
3. 搭配提示詞：`japandi style, wabi-sabi aesthetic, Nordic minimalism, natural materials, muted earth tones, imperfect textures, warm lighting, clean lines`

---

## 風格關鍵提示詞參考

中文提示詞：
```
侘寂風格, 北歐極簡, 自然材質, 大地色調, 溫暖光線, 木質紋理, 亞麻質感, 手作陶器, 不完美之美, 簡約線條
```

英文提示詞：
```
japandi interior design, wabi-sabi aesthetic, scandinavian minimalism, natural materials, earth tones, warm ambient lighting, wood grain texture, linen fabric, handmade ceramics, imperfect beauty, clean lines, muted palette
```

---

## Z-Image i2L 深入研究：網路討論與範例

### 技術架構與原理

Z-Image i2L (Image-to-LoRA) 由阿里巴巴通義實驗室於 2026 年 1 月 27 日發布，採用 Apache 2.0 開源授權（可商用）。

- **核心概念**：將 LoRA 創建視為直接推理任務 — 輸入圖片，輸出 LoRA 權重
- **參數規模**：16.1 億（1.61B）參數
- **前身**：基於 Qwen-Image-i2L（2025 年 12 月），遷移至 Z-Image 骨幹架構以大幅提升風格保持能力
- **影像編碼器**：使用 SigLIP2-G384 + DINOv3-7B 雙編碼器
- **開源位置**：
  - Hugging Face: https://huggingface.co/DiffSynth-Studio/Z-Image-i2L
  - ModelScope: https://www.modelscope.cn/models/DiffSynth-Studio/Z-Image-i2L
  - GitHub: https://github.com/Tongyi-MAI/Z-Image
  - 線上 Demo: https://huggingface.co/spaces/DiffSynth-Studio/Z-Image-i2L

### 官方效能數據

| 指標 | 數值 |
|------|------|
| 風格保留率 | 85%（水彩、寫實、極簡等風格） |
| 生成速度 | < 10 秒（cfg_scale=4, sigma_shift=8） |
| 比前代快 | 30%（對比 Qwen-Image-i2L） |
| 細節損失減少 | 15%（光影層次、色調都能精準複製） |
| 風格轉移細節保留提升 | 20% |
| 最低 VRAM 需求 | 16GB（消費級 GPU 可運行） |
| 產品設計週期縮短 | 30%-50%（阿里巴巴官方數據） |

### 官方示範的風格轉移範例

i2L 官方展示了以下風格轉移效果：

1. **柔和水彩風** — 從水彩畫生成 LoRA，將筆觸風格應用到貓、狗、人像等新主題
2. **高保真攝影** — LoRA 聚焦於質感、光線和照片級比例
3. **抽象平面設計** — 鮮豔的色塊風格
4. **高對比線稿** — 去除色彩，專注於線條
5. **奇幻藝術風** — 保留發光效果和魔法氛圍
6. **柔和花卉圖案** — 將花朵和有機形態融入背景與前景

### 關鍵使用技巧（Gold Standard 設定）

官方通過內部測試確定的最佳實踐：

```
推理設定：
- cfg_scale = 4
- sigma_shift = 8

關鍵技巧：
- LoRA 僅對正面提示詞 (positive prompt) 啟用
- 對負面提示詞 (negative prompt) 關閉 LoRA
→ 可顯著提升圖像保真度，防止風格溢出到不需要的偽影
```

### 社群討論與反饋

#### 正面評價
- 被社群認為是「遊戲規則改變者」
- CivitAI 用戶 Saruhey 評論：「This is what SD3 was supposed to be」
- 社群共識：Z-Image 已取代 Flux 成為 AI 藝術之王
- 一位用戶分享：使用 LoRA 後，提示詞從 80-100 tokens 降到 30-40 tokens，心力消耗大幅下降

#### 已知限制
- **過擬合風險**：單張圖片輸入可能導致生成圖像與原圖過於相似
- **複雜場景**：多人或擁擠背景的細節捕捉仍有改進空間
- 阿里巴巴已通過差異訓練（differential training）緩解過擬合問題

### ComfyUI 整合方案

#### 方案 A：ComfyUI_RH_ZImageI2L（專用 i2L 插件）

- **GitHub**: https://github.com/HM-RunningHub/ComfyUI_RH_ZImageI2L
- **安裝**：
  ```bash
  cd ComfyUI/custom_nodes
  git clone https://github.com/HM-RunningHub/ComfyUI_RH_ZImageI2L.git
  pip install -r requirements.txt
  ```
- **節點**：
  | 節點名稱 | 功能 |
  |---------|------|
  | ZImageI2L Loader | 初始化 i2L pipeline |
  | ZImageI2L LoRA Generator | 從參考圖生成 LoRA 權重 |
  | ZImageI2L Saver | 匯出生成的 LoRA 檔案 |
- **流程**：Loader → LoRA Generator（輸入參考圖）→ Saver
- **硬體需求**：24GB+ VRAM（RTX 4090 測試通過）
- **模型自動下載**：首次運行時從 ModelScope 自動下載並快取

#### 方案 B：Z-Image I2L2I Custom Node（Civitai 社群）

- **連結**: https://civitai.com/models/2345614/custom-nodes-z-image-i2l2i-single-pass-lora-create-and-use-and-image-selector
- **特色**：單次通過 LoRA 創建與使用（Single Pass），包含智能尺寸壓縮、強度歸一化等進階功能

### 其他 Z-Image ComfyUI 資源

- **官方 ComfyUI 教學**：https://docs.comfy.org/tutorials/image/z-image/z-image
- **官方範例**：https://comfyanonymous.github.io/ComfyUI_examples/z_image/
- **Custom Nodes 完整指南**：https://z-image.vip/blog/z-image-comfyui-custom-nodes-workflow
- **Z-Image Utilities（提示詞增強）**：https://github.com/Koko-boya/Comfyui-Z-Image-Utilities
- **AmazingZImageWorkflow（預設風格）**：https://github.com/martin-rizzo/AmazingZImageWorkflow

### 用於侘寂北歐風的建議做法

1. 準備一張理想的 Japandi / 侘寂北歐風室內設計參考圖（自然材質、大地色調、木質紋理、手作陶器）
2. 使用 Z-Image i2L 生成 LoRA（設定 `cfg_scale=4`, `sigma_shift=8`）
3. 推理時僅在正面提示詞啟用 LoRA，負面提示詞關閉
4. 搭配提示詞：`japandi interior, wabi-sabi aesthetic, scandinavian minimalism, natural wood, earth tones, muted palette, handmade ceramics, imperfect beauty`
5. 若效果偏過擬合，嘗試降低 LoRA 權重或加入更多樣的參考圖

---

## 參考資源

### Z-Image i2L 相關
- Z-Image i2L 官方發布文章：https://z-image.me/en/blog/z-image-i2l-released
- Hugging Face 模型頁面：https://huggingface.co/DiffSynth-Studio/Z-Image-i2L
- Hugging Face 線上 Demo：https://huggingface.co/spaces/DiffSynth-Studio/Z-Image-i2L
- ModelScope 模型頁面：https://www.modelscope.cn/models/DiffSynth-Studio/Z-Image-i2L
- GitHub 原始碼：https://github.com/Tongyi-MAI/Z-Image
- 風格捕捉詳解：https://zimagebase.com/blogs/z-image-i2l-image-to-lora
- 前代 Qwen-Image-i2L 指南：https://z-image.me/en/blog/Qwen-Image-i2L_en

### ComfyUI 整合
- ComfyUI_RH_ZImageI2L 插件：https://github.com/HM-RunningHub/ComfyUI_RH_ZImageI2L
- Civitai I2L2I 自定義節點：https://civitai.com/models/2345614/custom-nodes-z-image-i2l2i-single-pass-lora-create-and-use-and-image-selector
- 官方 ComfyUI 教學：https://docs.comfy.org/tutorials/image/z-image/z-image

### Z-Image 平台與 LoRA 資源
- Z-Image 官方平台：https://z-image.me
- Z-Image LoRA 指南：https://z-image.vip/blog/z-image-turbo-best-lora-collection-2025
- Z-Image Base LoRA 訓練指南：https://apatero.com/blog/z-image-base-lora-training-guide
- LoRA 訓練最佳實踐 2026：https://zimage.run/blog/best-practices-training-lora-models-z-image
- Civitai 社群：https://civitai.com
