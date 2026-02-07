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

## 參考資源

- Z-Image 官方平台：https://z-image.me
- Z-Image i2L 發布文章：https://z-image.me/en/blog/z-image-i2l-released
- Z-Image LoRA 指南：https://z-image.vip/blog/z-image-turbo-best-lora-collection-2025
- Civitai 社群：https://civitai.com
