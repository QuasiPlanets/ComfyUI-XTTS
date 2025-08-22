# XTTS Custom Node - Cursor Directory

## 📁 Directory Structure

This `.cursor` directory contains comprehensive documentation and tracking for the XTTS custom node, organized for optimal LLM understanding and future development.

### 📋 Files Overview

| File | Purpose | Last Updated |
|------|---------|--------------|
| `README.md` | This overview file | 2025-08-22 |
| `XTTS_DIAGNOSTIC_CODE_TRACKER.md` | Complete issue resolution history | 2025-08-22 |
| `TROUBLESHOOTING.md` | Common issues and solutions | 2025-08-22 |
| `XTTS_DEVELOPMENT_GUIDE.md` | Development patterns and best practices | 2025-08-22 |

## 🎯 Current Status

### ✅ Fully Operational System
- **Model**: XTTS-v2 HiFiGAN (v2.0.3)
- **Architecture**: HiFiGAN-based (not diffusion-based)
- **Dependencies**: transformers==4.51.0, TTS==0.22.0
- **Audio Quality**: Clean, natural speech output
- **Text Processing**: Intelligent chunking (250 char chunks)

### 🔧 Key Features
- **Auto-Download**: XTTS-v2 model downloads automatically
- **Text Chunking**: Handles long text without truncation
- **Multi-Language**: 17 languages supported
- **ComfyUI Integration**: Seamless node integration

## 🚨 Critical Information

### Dependencies
```txt
# CRITICAL: transformers 4.52+ causes corrupted audio
transformers==4.51.0
TTS==0.22.0
```

### Model Details
- **Repository**: `coqui/XTTS-v2`
- **Revision**: `v2.0.3`
- **Size**: 1.87GB
- **Hash**: `4736c072db0c929ca6be932680d0d406`
- **Architecture**: HiFiGAN-based

### Auto-Download Configuration
```python
snapshot_download(repo_id="coqui/XTTS-v2",revision="v2.0.3",local_dir=pretrained_models_path)
```

## 📊 Issue Resolution History

### Major Issues Resolved
1. **PyTorch 2.6+ Compatibility** - Fixed `weights_only=False` parameter
2. **Model Architecture Mismatch** - Switched from XTTS-v1 to XTTS-v2
3. **Transformers Compatibility** - Downgraded to 4.51.0 for clean audio
4. **Text Truncation** - Implemented intelligent chunking
5. **Auto-Download Setup** - Configured for replicability

### Current Status: ✅ Production Ready
- All critical issues resolved
- 100% replicable installation
- Clean audio output confirmed
- Comprehensive documentation complete

## 🔍 Quick Reference

### Verification Commands
```bash
# Check setup
python verify_setup.py

# Check transformers version
pip show transformers

# Check model architecture
python -c "import torch; checkpoint = torch.load('pretrained_models/model.pth', map_location='cpu', weights_only=False); print('Has hifigan:', any('hifigan_decoder' in k for k in checkpoint['model'].keys()))"
```

### Common Issues
- **Corrupted Audio**: Ensure transformers==4.51.0
- **Missing Keys**: Wrong model architecture (use XTTS-v2)
- **Download Failures**: Use HF mirror or manual download
- **Import Errors**: Reinstall requirements.txt

## 📈 Development Patterns

### Text Chunking Implementation
```python
max_chars_per_chunk = 250
# Split into sentences, process chunks, concatenate audio
```

### Model Loading Pattern
```python
# Check if model exists, download if needed, load with correct config
if not os.path.isfile(os.path.join(pretrained_models_path,"model.pth")):
    snapshot_download(repo_id="coqui/XTTS-v2",revision="v2.0.3",local_dir=pretrained_models_path)
```

### Error Handling
- Graceful fallback for download failures
- Architecture verification before loading
- Memory cleanup after inference

## 🎯 Future Development

### Recommended Improvements
1. **Caching**: Implement model caching for faster loading
2. **Batch Processing**: Support for multiple audio files
3. **Quality Settings**: Adjustable audio quality parameters
4. **Language Detection**: Automatic language detection

### Maintenance Tasks
1. **Dependency Updates**: Monitor for compatible versions
2. **Model Updates**: Check for new XTTS versions
3. **Performance Optimization**: Profile and optimize inference
4. **Documentation Updates**: Keep guides current

## 📞 Support Resources

### Documentation Files
- `XTTS_DIAGNOSTIC_CODE_TRACKER.md` - Complete development history
- `TROUBLESHOOTING.md` - Common issues and solutions
- `XTTS_DEVELOPMENT_GUIDE.md` - Development patterns

### External Resources
- [Main README](../README.md) - User installation guide
- [Setup Guide](../SETUP_GUIDE.md) - Comprehensive setup instructions
- [Verification Script](../verify_setup.py) - Automated setup verification

---

**🎯 This directory provides complete context for LLMs working with the XTTS custom node!**
