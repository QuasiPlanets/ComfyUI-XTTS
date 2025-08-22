# XTTS-v2 Setup Guide

## 🚀 Complete Replicable Setup

This guide ensures **100% replicable** XTTS-v2 installations with clean audio output.

## 📋 Prerequisites

### System Requirements
- **Python**: 3.8+ (tested with 3.10.12)
- **GPU**: NVIDIA GPU with CUDA support (recommended)
- **RAM**: 8GB+ (16GB+ recommended)
- **Storage**: 5GB+ free space for model

### FFmpeg Installation
**Linux:**
```bash
apt update && apt install ffmpeg
```

**Windows:**
Install via [WingetUI](https://github.com/marticliment/WingetUI) or download from [ffmpeg.org](https://ffmpeg.org/download.html)

## 🔧 Installation Steps

### 1. Clone Repository
```bash
git clone https://github.com/AIFSH/ComfyUI-XTTS.git
cd ComfyUI-XTTS
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

**Critical Dependencies:**
- `transformers==4.51.0` - **CRITICAL**: Versions 4.52+ cause corrupted audio
- `TTS==0.22.0` - Compatible with XTTS-v2
- All other dependencies for 17-language support

### 3. Verify Setup
```bash
python verify_setup.py
```

**Expected Output:**
```
🎉 All 6 checks passed! XTTS-v2 is ready to use.
✅ Setup is complete and replicable!
```

## 🤖 Auto-Download Features

### Model Download
- **Model**: XTTS-v2 HiFiGAN (1.87GB)
- **Revision**: v2.0.3 (stable)
- **Auto-Download**: Downloads automatically on first use
- **Location**: `pretrained_models/` directory

### Configuration
- **Architecture**: HiFiGAN-based (not diffusion-based)
- **Text Chunking**: 250 character chunks for long text
- **Audio Quality**: High-quality, clean output

## 🌐 Network Issues

### China/Regional Restrictions
If you have issues accessing Hugging Face:

1. **Use HF Mirror:**
   ```bash
   export HF_ENDPOINT=https://hf-mirror.com
   ```

2. **Manual Download:**
   - Download from: [Quark Cloud](https://pan.quark.cn/s/43917b8b8572)
   - Extract `pretrained_models` folder to `ComfyUI-XTTS/` directory

## 🎯 Usage

### ComfyUI Integration
1. **Restart ComfyUI** after installation
2. **XTTS nodes** will appear in the node menu
3. **First use** will trigger auto-download
4. **Subsequent uses** will load cached model

### Node Types
- **XTTS_INFER**: Basic text-to-speech
- **XTTS_INFER_SRT**: Subtitle file processing
- **PreViewAudio**: Audio preview

### Parameters
- `temperature`: 0.65 (default) - Speech randomness
- `length_penalty`: 1.0 (default) - Output length
- `repetition_penalty`: 2.0 (default) - Prevent repetition
- `top_k`: 50 (default) - Token selection
- `top_p`: 0.8 (default) - Nucleus sampling
- `speed`: 1.0 (default) - Speech speed

## 🔍 Troubleshooting

### Common Issues

#### 1. Corrupted Audio Output
**Symptoms:** Undiscernible, distorted speech
**Solution:** Ensure `transformers==4.51.0`
```bash
pip install transformers==4.51.0
```

#### 2. Model Download Fails
**Symptoms:** "No target revision found" error
**Solution:** Check internet connection or use HF mirror
```bash
export HF_ENDPOINT=https://hf-mirror.com
```

#### 3. Missing Dependencies
**Symptoms:** Import errors
**Solution:** Reinstall requirements
```bash
pip install -r requirements.txt
```

#### 4. Wrong Model Architecture
**Symptoms:** "Missing key(s)" errors
**Solution:** Delete `pretrained_models/` and restart (auto-downloads correct model)

### Verification Commands
```bash
# Check transformers version
pip show transformers

# Verify model architecture
python verify_setup.py

# Check model files
ls -la pretrained_models/
```

## 📊 Performance

### Expected Results
- **Model Loading**: ~30 seconds (first time)
- **Audio Generation**: ~8 seconds per chunk
- **Memory Usage**: ~2.5GB VRAM
- **Audio Quality**: High-quality, natural speech

### Supported Languages
English (en), Spanish (es), French (fr), German (de), Italian (it), Portuguese (pt), Polish (pl), Turkish (tr), Russian (ru), Dutch (nl), Czech (cs), Arabic (ar), Chinese (zh-cn), Japanese (ja), Hungarian (hu), Korean (ko), Hindi (hi)

## 🎉 Success Indicators

### ✅ Working Setup
- Clean, natural speech output
- No "Missing key(s)" errors
- Text chunking works (10+ chunks)
- Model loads without download on subsequent uses

### ❌ Issues to Fix
- Corrupted/undiscernible audio
- Model download errors
- Import/dependency errors
- Wrong architecture errors

## 📞 Support

### Verification Script
Run `python verify_setup.py` to diagnose issues

### Documentation
- [Main README](README.md)
- [Troubleshooting Guide](.cursor/TROUBLESHOOTING.md)
- [Development Guide](.cursor/XTTS_DEVELOPMENT_GUIDE.md)

### Community
- WeChat Group: See README for QR code
- GitHub Issues: Report bugs and feature requests

---

**🎯 This setup ensures 100% replicable XTTS-v2 installations with clean audio output!**
