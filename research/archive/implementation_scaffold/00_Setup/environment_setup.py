#!/usr/bin/env python3
"""
Environment Setup Script for CSE499 Project
Run this script in Google Colab to set up the environment
"""

def setup_environment():
    """Set up the complete environment for CSE499 project."""
    
    print("=" * 60)
    print("CSE499: EHR-Based Pre-Consultation Medical Documentation System")
    print("Environment Setup")
    print("=" * 60)
    
    # Step 1: Install system dependencies
    print("\n[1/5] Installing system dependencies...")
    import subprocess
    subprocess.run(["apt-get", "update"], capture_output=True)
    subprocess.run(["apt-get", "install", "-y", "ffmpeg"], capture_output=True)
    print("✓ System dependencies installed")
    
    # Step 2: Install Python packages
    print("\n[2/5] Installing Python packages...")
    import subprocess
    packages = [
        "torch",
        "transformers",
        "datasets",
        "librosa",
        "soundfile",
        "yt-dlp",
        "jiwer",
        "seqeval",
        "pandas",
        "numpy",
        "matplotlib",
        "tqdm",
        "pyyaml",
        "ipywidgets"
    ]
    
    for pkg in packages:
        subprocess.run(["pip", "install", "-q", pkg])
    print("✓ Python packages installed")
    
    # Step 3: Check GPU availability
    print("\n[3/5] Checking GPU availability...")
    import torch
    if torch.cuda.is_available():
        print(f"✓ GPU available: {torch.cuda.get_device_name(0)}")
        print(f"  CUDA version: {torch.version.cuda}")
        print(f"  GPU memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")
    else:
        print("⚠ No GPU available - training will be slow")
    
    # Step 4: Verify installations
    print("\n[4/5] Verifying installations...")
    try:
        import transformers
        import librosa
        import soundfile
        import jiwer
        print("✓ All core packages verified")
    except ImportError as e:
        print(f"⚠ Import error: {e}")
    
    # Step 5: Mount Google Drive
    print("\n[5/5] Google Drive setup...")
    from google.colab import drive
    
    try:
        drive.mount('/content/drive')
        print("✓ Google Drive mounted at /content/drive")
    except:
        print("⚠ Could not mount Google Drive automatically")
        print("  Run: drive.mount('/content/drive') manually if needed")
    
    print("\n" + "=" * 60)
    print("Setup complete! Ready to start CSE499 project.")
    print("=" * 60)
    
    return True


def install_packages():
    """Quick package installation for existing environment."""
    import subprocess
    import sys
    
    print("Installing Python packages...")
    
    packages = [
        "torch>=2.0.0",
        "transformers>=4.30.0",
        "datasets>=2.0.0",
        "accelerate>=0.20.0",
        "evaluate>=0.4.0",
        "seqeval>=1.2.2",
        "librosa>=0.10.0",
        "soundfile>=0.12.0",
        "yt-dlp>=2023.12.30",
        "jiwer>=3.0.0",
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "matplotlib>=3.7.0",
        "tqdm>=4.65.0",
        "pyyaml>=6.0",
        "ipywidgets>=8.1.0"
    ]
    
    for pkg in packages:
        print(f"  Installing {pkg.split('>=')[0]}...", end=" ")
        result = subprocess.run([sys.executable, "-m", "pip", "install", "-q", pkg], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✓")
        else:
            print(f"⚠ ({result.returncode})")
    
    print("\n✓ Package installation complete!")


if __name__ == "__main__":
    # Check if running in Colab
    try:
        from google.colab import drive
        print("Running in Google Colab - running full setup...")
        setup_environment()
    except ImportError:
        print("Not in Google Colab - running quick package install...")
        install_packages()
