# Paper Translator

一款优雅的 **macOS 风格** PDF 论文双语对照阅读器，让论文阅读更加高效。

![Platform](https://img.shields.io/badge/platform-Windows-blue)
![Python](https://img.shields.io/badge/Python-3.10+-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ 特性

- 🎨 **Apple 风格界面** — 简洁优雅的 macOS 设计语言，沉浸式阅读体验
- 📄 **PDF 拖拽上传** — 一步拖入论文文件，即刻开始阅读
- 🔄 **双语对照** — 原文与译文左右分栏，阅读流畅不打断
- 🔃 **同步滚动** — 滚动原文时译文自动跟随，阅读效率倍增
- 🎛️ **可调布局** — 拖拽分割线调整左右比例，随心所欲
- 🤖 **智能翻译** — Gemini 2.5 主力 + Google Translate 降级，保证翻译不中断
- 📚 **论文优化** — 自动识别图表标题、跳过参考文献，专注核心内容
- 💾 **翻译缓存** — 相同内容自动缓存，重复阅读无需等待

## 🚀 快速开始

### 方式一：运行安装脚本（推荐）

```bash
install_windows.bat
```

### 方式二：手动安装

```bash
# 1. 创建虚拟环境
python -m venv venv
venv\Scripts\pip activate

# 2. 安装依赖
pip install -r requirements.txt

# 3. 配置翻译 API
copy config\config.yaml.example config\config.yaml
# 编辑 config.yaml，填入你的 Gemini API Key

# 4. 启动程序
python main.py
```

## ⚙️ 配置说明

### 获取 Gemini API Key

1. 访问 [Google AI Studio](https://aistudio.google.com/app/apikey)
2. 点击「Create API Key」
3. 复制 Key 到 `config/config.yaml`：

```yaml
translator:
  gemini:
    api_key: "YOUR_API_KEY_HERE"
```

> 💡 **提示**：Gemini 有免费配额，超出后自动降级到 Google Translate（免费），翻译服务不中断。

### 完整配置项

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `translator.primary` | 主翻译引擎 `gemini` 或 `google` | `gemini` |
| `translator.gemini.model` | Gemini 模型名称 | `gemini-2.5-flash-preview-0520` |
| `translator.gemini.temperature` | 生成温度 0.0-1.0 | `0.3` |
| `pdf.translate_figure_captions` | 翻译图表标题 | `true` |
| `pdf.skip_references` | 跳过参考文献章节 | `true` |
| `ui.sync_scroll` | 启用滚动同步 | `true` |
| `cache.enabled` | 启用翻译缓存 | `true` |

## 📖 使用方法

1. **打开 PDF** — 拖拽文件到窗口，或点击「浏览文件」
2. **阅读对照** — 左侧原文，右侧译文
3. **调整布局** — 拖拽中间分割线调整比例
4. **同步滚动** — 开启时滚动一侧，另一侧自动跟随
5. **配置设置** — 点击右上角⚙️按钮

## 🛠️ 技术栈

- **GUI 框架**: [PySide6](https://wiki.qt.io/PySide6) — 官方 Qt Python 绑定
- **PDF 解析**: [PyMuPDF](https://pymupdf.readthedocs.io/) (fitz) — 高性能 PDF 处理
- **翻译引擎**: Google Gemini API + Google Translate
- **打包工具**: [PyInstaller](https://pyinstaller.org/)

## 📁 项目结构

```
paper-translator/
├── main.py                 # 程序入口
├── requirements.txt       # Python 依赖
├── config/
│   └── config.yaml.example # 配置模板
├── src/
│   ├── core/
│   │   ├── pdf_parser.py   # PDF 解析与文本提取
│   │   └── translator.py   # 翻译引擎（含缓存）
│   ├── gui/
│   │   └── main_window.py  # 主界面
│   └── utils/
│       └── config_loader.py # 配置加载
├── install_windows.bat     # Windows 安装脚本
├── run_windows.bat         # Windows 启动脚本
└── paper_translator.spec  # PyInstaller 打包配置
```

## ⚠️ 常见问题

**Q: 翻译失败怎么办？**
> 程序会自动降级到 Google Translate（免费），保证翻译不中断。

**Q: 扫描版 PDF 无法读取？**
> 目前仅支持文字版 PDF。扫描版需先 OCR 转换。

**Q: 翻译结果不满意？**
> 可以在 `config.yaml` 调整 `temperature` 参数，较低值更精确，较高值更有创造性。

## 📄 许可证

MIT License — 自由使用、修改和分发。

---

*让论文阅读更优雅* 🎓