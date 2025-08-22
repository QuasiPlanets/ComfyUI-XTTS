# XTTS System Tracker

## 🎯 System Overview

**Status**: ✅ PRODUCTION READY  
**Last Updated**: 2025-08-22  
**Version**: XTTS-v2 HiFiGAN v2.0.3  
**Architecture**: HiFiGAN-based (not diffusion-based)

## 📊 Current System State

### ✅ Operational Components

| Component | Status | Version | Details |
|-----------|--------|---------|---------|
| **Model** | ✅ Working | XTTS-v2 v2.0.3 | HiFiGAN architecture, 1.87GB |
| **Transformers** | ✅ Compatible | 4.51.0 | Critical: 4.52+ causes corrupted audio |
| **TTS Library** | ✅ Compatible | 0.22.0 | XTTS-v2 support |
| **Text Chunking** | ✅ Working | 250 chars | Intelligent sentence splitting |
| **Auto-Download** | ✅ Working | v2.0.3 | Downloads on first use |
| **Audio Quality** | ✅ Clean | Natural speech | No corruption or distortion |

### 🔧 Configuration Details

#### Model Configuration
```json
{
  "model": "xtts",
  "gpt_number_text_tokens": 6681,
  "gpt_start_text_token": null,
  "architecture": "hifigan"
}
```

#### Download Configuration
```python
snapshot_download(
    repo_id="coqui/XTTS-v2",
    revision="v2.0.3",
    local_dir=pretrained_models_path
)
```

#### Text Processing Configuration
```python
max_chars_per_chunk = 250
enable_text_splitting = False  # Manual chunking
```

## 📁 File Structure

### Core Files
```
custom_nodes/ComfyUI-XTTS/
├── nodes.py                    # Main node implementation
├── requirements.txt            # Dependencies (transformers==4.51.0)
├── README.md                   # User installation guide
├── SETUP_GUIDE.md             # Comprehensive setup guide
├── verify_setup.py            # Setup verification script
├── pretrained_models/         # Model files (1.87GB total)
│   ├── model.pth              # Main model (1.78GB)
│   ├── config.json            # Model configuration
│   ├── vocab.json             # Vocabulary file
│   ├── speakers_xtts.pth      # Speaker embeddings
│   ├── dvae.pth               # DVAE model
│   └── mel_stats.pth          # Mel statistics
└── .cursor/                   # LLM documentation
    ├── README.md              # This overview
    ├── SYSTEM_TRACKER.md      # This file
    ├── XTTS_DIAGNOSTIC_CODE_TRACKER.md
    ├── TROUBLESHOOTING.md
    └── XTTS_DEVELOPMENT_GUIDE.md
```

## 🔍 Verification Commands

### Quick Health Check
```bash
# Verify setup
python verify_setup.py

# Check transformers version
pip show transformers | grep Version

# Check model architecture
python -c "
import torch
checkpoint = torch.load('pretrained_models/model.pth', map_location='cpu', weights_only=False)
model_state = checkpoint['model']
has_hifigan = any('hifigan_decoder' in k for k in model_state.keys())
has_diffusion = any('diffusion_decoder' in k for k in model_state.keys())
print(f'HiFiGAN: {has_hifigan}, Diffusion: {has_diffusion}')
"
```

### Model Verification
```bash
# Check model hash
md5sum pretrained_models/model.pth
# Expected: 4736c072db0c929ca6be932680d0d406

# Check model size
ls -lh pretrained_models/model.pth
# Expected: ~1.87GB
```

## 🚨 Critical Dependencies

### Must-Have Versions
```txt
transformers==4.51.0  # CRITICAL: 4.52+ causes corrupted audio
TTS==0.22.0          # XTTS-v2 compatibility
torch>=1.0           # PyTorch support
torchaudio>=1.0      # Audio processing
numpy>=1.17          # Numerical operations
librosa>=0.8         # Audio analysis
```

### Optional Dependencies
```txt
ffmpeg               # Audio processing (system dependency)
cuda                 # GPU acceleration (optional)
```

## 📈 Performance Metrics

### Expected Performance
- **Model Loading**: ~30 seconds (first time)
- **Audio Generation**: ~8 seconds per chunk
- **Memory Usage**: ~2.5GB VRAM
- **Text Processing**: 250 characters per chunk
- **Audio Quality**: High-quality, natural speech

### Supported Languages
English (en), Spanish (es), French (fr), German (de), Italian (it), Portuguese (pt), Polish (pl), Turkish (tr), Russian (ru), Dutch (nl), Czech (cs), Arabic (ar), Chinese (zh-cn), Japanese (ja), Hungarian (hu), Korean (ko), Hindi (hi)

## 🔧 Node Types

### Available Nodes
1. **XTTS_INFER**: Basic text-to-speech conversion
2. **XTTS_INFER_SRT**: Subtitle file processing
3. **PreViewAudio**: Audio preview and playback

### Node Parameters
- `temperature`: 0.65 (speech randomness)
- `length_penalty`: 1.0 (output length)
- `repetition_penalty`: 2.0 (prevent repetition)
- `top_k`: 50 (token selection)
- `top_p`: 0.8 (nucleus sampling)
- `speed`: 1.0 (speech speed)

## 🎯 Success Indicators

### ✅ Working System
- Clean, natural speech output
- No "Missing key(s)" errors
- Text chunking processes 10+ chunks
- Model loads without download on subsequent uses
- Verification script passes all checks

### ❌ System Issues
- Corrupted/undiscernible audio
- Model download errors
- Import/dependency errors
- Wrong architecture errors
- Text truncation warnings

## 🔄 Maintenance Tasks

### Regular Checks
1. **Dependency Updates**: Monitor for compatible versions
2. **Model Updates**: Check for new XTTS versions
3. **Performance Monitoring**: Track inference times
4. **Error Logging**: Monitor for new issues

### Update Procedures
1. **Dependencies**: Test new versions before updating
2. **Model**: Verify architecture compatibility
3. **Code**: Test with verification script
4. **Documentation**: Update guides and trackers

## 📞 Support Resources

### Documentation
- `README.md` - User installation guide
- `SETUP_GUIDE.md` - Comprehensive setup instructions
- `verify_setup.py` - Automated verification
- `.cursor/` - LLM documentation and tracking

### Troubleshooting
- `TROUBLESHOOTING.md` - Common issues and solutions
- `XTTS_DIAGNOSTIC_CODE_TRACKER.md` - Complete issue history
- `XTTS_DEVELOPMENT_GUIDE.md` - Development patterns

### Community
- GitHub Issues: Bug reports and feature requests
- WeChat Group: Community support (see main README)

---

**🎯 This tracker provides complete system context for LLMs and developers!**
