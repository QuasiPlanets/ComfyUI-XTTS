#!/usr/bin/env python3
"""
XTTS Setup Verification Script
Verifies that all dependencies and configurations are correct for XTTS-v2 operation.
"""

import sys
import os
import subprocess
import importlib

def check_python_version():
    """Check Python version compatibility."""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Requires Python 3.8+")
        return False

def check_critical_dependencies():
    """Check critical dependencies for XTTS-v2."""
    print("\n📦 Checking critical dependencies...")
    
    critical_deps = {
        'transformers': '4.51.0',  # CRITICAL: 4.52+ causes corrupted audio
        'TTS': '0.22.0',
        'torch': None,  # Any version
        'torchaudio': None,  # Any version
        'numpy': None,  # Any version
        'librosa': None,  # Any version
    }
    
    all_good = True
    
    for package, required_version in critical_deps.items():
        try:
            module = importlib.import_module(package)
            if hasattr(module, '__version__'):
                version = module.__version__
                if required_version:
                    if version == required_version:
                        print(f"✅ {package} {version} - Correct version")
                    else:
                        print(f"❌ {package} {version} - Requires {required_version}")
                        all_good = False
                else:
                    print(f"✅ {package} {version} - Installed")
            else:
                print(f"✅ {package} - Installed (version unknown)")
        except ImportError:
            print(f"❌ {package} - Not installed")
            all_good = False
    
    return all_good

def check_model_files():
    """Check if XTTS-v2 model files are present."""
    print("\n🤖 Checking XTTS-v2 model files...")
    
    model_path = os.path.join(os.path.dirname(__file__), "pretrained_models")
    required_files = [
        "model.pth",
        "config.json", 
        "vocab.json",
        "speakers_xtts.pth",
        "dvae.pth",
        "mel_stats.pth"
    ]
    
    # Expected model hash for verification
    expected_hash = "4736c072db0c929ca6be932680d0d406"
    
    all_present = True
    
    for file in required_files:
        file_path = os.path.join(model_path, file)
        if os.path.exists(file_path):
            size = os.path.getsize(file_path) / (1024 * 1024)  # MB
            print(f"✅ {file} - {size:.1f} MB")
            
            # Check model.pth hash
            if file == "model.pth":
                import hashlib
                with open(file_path, 'rb') as f:
                    file_hash = hashlib.md5(f.read()).hexdigest()
                if file_hash == expected_hash:
                    print(f"   ✅ Model hash verified: {file_hash}")
                else:
                    print(f"   ❌ Model hash mismatch: {file_hash} (expected: {expected_hash})")
                    all_present = False
        else:
            print(f"❌ {file} - Missing")
            all_present = False
    
    return all_present

def check_model_architecture():
    """Verify the model has correct HiFiGAN architecture."""
    print("\n🏗️ Checking model architecture...")
    
    try:
        import torch
        model_path = os.path.join(os.path.dirname(__file__), "pretrained_models", "model.pth")
        
        if not os.path.exists(model_path):
            print("❌ Model file not found - will download on first use")
            return True  # Not an error, will auto-download
        
        checkpoint = torch.load(model_path, map_location='cpu', weights_only=False)
        model_state = checkpoint['model']
        
        # Check for HiFiGAN components
        has_hifigan = any('hifigan_decoder' in k for k in model_state.keys())
        has_diffusion = any('diffusion_decoder' in k for k in model_state.keys())
        
        if has_hifigan and not has_diffusion:
            print("✅ HiFiGAN-based architecture (XTTS-v2) - Correct")
            return True
        elif has_diffusion and not has_hifigan:
            print("❌ Diffusion-based architecture (XTTS-v1) - Wrong model")
            return False
        else:
            print("❓ Unknown architecture - Model may be corrupted")
            return False
            
    except Exception as e:
        print(f"❌ Error checking model architecture: {e}")
        return False

def check_auto_download_config():
    """Check auto-download configuration."""
    print("\n⬇️ Checking auto-download configuration...")
    
    nodes_file = os.path.join(os.path.dirname(__file__), "nodes.py")
    
    try:
        with open(nodes_file, 'r') as f:
            content = f.read()
            
        if 'coqui/XTTS-v2' in content and 'v2.0.3' in content:
            print("✅ Auto-download configured for XTTS-v2 v2.0.3")
            return True
        else:
            print("❌ Auto-download not configured correctly")
            return False
            
    except Exception as e:
        print(f"❌ Error checking auto-download config: {e}")
        return False

def check_text_chunking():
    """Check text chunking implementation."""
    print("\n📝 Checking text chunking implementation...")
    
    nodes_file = os.path.join(os.path.dirname(__file__), "nodes.py")
    
    try:
        with open(nodes_file, 'r') as f:
            content = f.read()
            
        if 'max_chars_per_chunk = 250' in content and 'enable_text_splitting=False' in content:
            print("✅ Text chunking implemented (250 char chunks)")
            return True
        else:
            print("❌ Text chunking not properly implemented")
            return False
            
    except Exception as e:
        print(f"❌ Error checking text chunking: {e}")
        return False

def main():
    """Main verification function."""
    print("🔍 XTTS-v2 Setup Verification")
    print("=" * 50)
    
    checks = [
        check_python_version(),
        check_critical_dependencies(),
        check_model_files(),
        check_model_architecture(),
        check_auto_download_config(),
        check_text_chunking()
    ]
    
    print("\n" + "=" * 50)
    print("📊 Verification Summary")
    print("=" * 50)
    
    passed = sum(checks)
    total = len(checks)
    
    if passed == total:
        print(f"🎉 All {total} checks passed! XTTS-v2 is ready to use.")
        print("\n✅ Setup is complete and replicable!")
        return True
    else:
        print(f"⚠️ {passed}/{total} checks passed. Some issues need attention.")
        print("\n📋 To fix issues:")
        print("1. Run: pip install -r requirements.txt")
        print("2. Restart ComfyUI")
        print("3. Run this script again")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
