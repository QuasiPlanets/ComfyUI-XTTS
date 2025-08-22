# ComfyUI-XTTS
a custom comfyui node for [coqui-ai/TTS](https://github.com/coqui-ai/TTS.git)'s xtts module! support 17 languages voice cloning and tts

 English (en), Spanish (es), French (fr), German (de), Italian (it), Portuguese (pt), Polish (pl), Turkish (tr), Russian (ru), Dutch (nl), Czech (cs), Arabic (ar), Chinese (zh-cn), Japanese (ja), Hungarian (hu), Korean (ko) Hindi (hi)

<div>
  <figure>
  <img alt='webpage' src="web.png?raw=true" width="600px"/>
  <figure>
</div>

# Disclaimer  / 免责声明
We do not hold any responsibility for any illegal usage of the codebase. Please refer to your local laws about DMCA and other related laws.
我们不对代码库的任何非法使用承担任何责任. 请参阅您当地关于 DMCA (数字千年法案) 和其他相关法律法规.


## Features
- `srt` file for subtitle was supported
- mutiple speaker was supported in finetune and inference by `srt`
- huge comfyui custom nodes can merge in xtts

## How to use
make sure `ffmpeg` is worked in your commandline
for Linux
```
apt update
apt install ffmpeg
```
for Windows,you can install `ffmpeg` by [WingetUI](https://github.com/marticliment/WingetUI) automatically

then!
```
git clone https://github.com/AIFSH/ComfyUI-XTTS.git
cd ComfyUI-XTTS
pip install -r requirements.txt
```

## 🚀 Auto-Setup Features
- **✅ Auto-Download**: XTTS-v2 model (1.87GB) downloads automatically on first use
- **✅ Auto-Configuration**: Correct model architecture and settings applied automatically
- **✅ Text Chunking**: Intelligent text splitting for long content (250 char chunks)
- **✅ Clean Audio**: Compatible transformers version (4.51.0) for high-quality output

## 📋 Critical Dependencies
The requirements.txt includes the **exact working versions**:
- `transformers==4.51.0` - **CRITICAL**: Versions 4.52+ cause corrupted audio
- `TTS==0.22.0` - Compatible with XTTS-v2
- All other dependencies for 17-language support

## 🌐 Model Download

### Auto-Download (Recommended)
`weights` will be downloaded from huggingface automatically on first use!
- **Model**: XTTS-v2 HiFiGAN (1.87GB)
- **Revision**: v2.0.3 (stable)
- **Architecture**: HiFiGAN-based (not diffusion-based)
- **Hash**: `4736c072db0c929ca6be932680d0d406`

### Manual Download (If Auto-Download Fails)

#### Option 1: Hugging Face Direct Download
```bash
# Download from Hugging Face
git clone https://huggingface.co/coqui/XTTS-v2
cd XTTS-v2
git checkout v2.0.3
# Copy pretrained_models folder to ComfyUI-XTTS/
cp -r . ../ComfyUI-XTTS/pretrained_models/
```

#### Option 2: Hugging Face Web Download
1. Visit: https://huggingface.co/coqui/XTTS-v2
2. Click "Files and versions" tab
3. Select "v2.0.3" branch
4. Download all files in the root directory
5. Extract to `ComfyUI-XTTS/pretrained_models/` folder

#### Option 3: China/Regional Mirror
If you're in China or have network restrictions:

**HF Mirror:**
```bash
export HF_ENDPOINT=https://hf-mirror.com
# Then run auto-download or manual download
```

**Quark Cloud (Chinese):**
- Download from: [Quark Cloud](https://pan.quark.cn/s/43917b8b8572)
- Extract `pretrained_models` folder to `ComfyUI-XTTS/` directory

#### Option 4: Direct File Download
Download these specific files to `pretrained_models/`:
- [model.pth](https://huggingface.co/coqui/XTTS-v2/resolve/v2.0.3/model.pth) (1.87GB)
- [config.json](https://huggingface.co/coqui/XTTS-v2/resolve/v2.0.3/config.json)
- [vocab.json](https://huggingface.co/coqui/XTTS-v2/resolve/v2.0.3/vocab.json)
- [speakers_xtts.pth](https://huggingface.co/coqui/XTTS-v2/resolve/v2.0.3/speakers_xtts.pth)
- [dvae.pth](https://huggingface.co/coqui/XTTS-v2/resolve/v2.0.3/dvae.pth)
- [mel_stats.pth](https://huggingface.co/coqui/XTTS-v2/resolve/v2.0.3/mel_stats.pth)

### Verification
After manual download, verify the setup:
```bash
python verify_setup.py
```

## Tutorial
[Demo](https://www.bilibili.com/video/BV1Wt421u7tu)

## Params

- `temperature`: The softmax temperature of the autoregressive model. Defaults to 0.65.

- `length_penalty`: A length penalty applied to the autoregressive decoder. Higher settings causes the model to produce more terse outputs. Defaults to 1.0.

- `repetition_penalty`: A penalty that prevents the autoregressive decoder from repeating itself during decoding. Can be used to reduce the incidence of long silences or “uhhhhhhs”, etc. Defaults to 2.0.

- `top_k`: Lower values mean the decoder produces more “likely” (aka boring) outputs. Defaults to 50.

- `top_p`: Lower values mean the decoder produces more “likely” (aka boring) outputs. Defaults to 0.8.

- `speed`: The speed rate of the generated audio. Defaults to 1.0. (can produce artifacts if far from 1.0)


## WeChat Group && Donate
<div>
  <figure>
  <img alt='Wechat' src="wechat.jpg?raw=true" width="300px"/>
  <img alt='donate' src="donate.jpg?raw=true" width="300px"/>
  <figure>
</div>

## Thanks
[coqui-ai/TTS](https://github.com/coqui-ai/TTS.git)
# XTTS Development
