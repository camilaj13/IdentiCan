#!/usr/bin/env bash
# ============================================================================
# Download Pet-ReID-IMAG model weights
#
# Source: https://github.com/muzishen/Pet-ReID-IMAG
# Google Drive: https://drive.google.com/drive/folders/1_7pdSRTvD_XdTu8z0MxrM9PDoEuX-tjf
# ============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# -------------------------------------------------------------------
# 1) Pretrained backbone (ResNeSt-101 ImageNet weights)
#    Downloaded from the official ResNeSt GitHub release.
# -------------------------------------------------------------------
PRETRAIN_DIR="$SCRIPT_DIR/pretrain"
mkdir -p "$PRETRAIN_DIR"

RESNEST101_URL="https://github.com/zhanghang1989/ResNeSt/releases/download/weights_step1/resnest101-22405ba7.pth"
RESNEST101_FILE="$PRETRAIN_DIR/resnest101-22405ba7.pth"

if [ ! -f "$RESNEST101_FILE" ]; then
    echo ">>> Downloading ResNeSt-101 pretrained backbone..."
    wget -q --show-progress -O "$RESNEST101_FILE" "$RESNEST101_URL"
    echo "    Saved to $RESNEST101_FILE"
else
    echo ">>> ResNeSt-101 backbone already exists: $RESNEST101_FILE"
fi

# -------------------------------------------------------------------
# 2) Trained Pet-ReID model weights (from Google Drive)
#    These are the actual pet-biometric-trained weights that give the
#    best identification accuracy. Requires `pip install gdown`.
#
#    Google Drive folder contains:
#      logs/s101_224/model_final.pth  (ResNeSt-101, 224x224 input)
#      logs/s101_256/model_final.pth  (ResNeSt-101, 256x256 input)  <-- primary
#      logs/s101_288/model_final.pth  (ResNeSt-101, 288x288 input)
#      logs/s200_224/model_final.pth  (ResNeSt-200, 224x224 input)
# -------------------------------------------------------------------
GDRIVE_FOLDER_ID="1_7pdSRTvD_XdTu8z0MxrM9PDoEuX-tjf"
GDRIVE_URL="https://drive.google.com/drive/folders/${GDRIVE_FOLDER_ID}"
LOGS_DIR="$SCRIPT_DIR/logs"

if ! command -v gdown &> /dev/null; then
    echo ""
    echo ">>> gdown is not installed. Installing..."
    pip install gdown
fi

# Check if the primary model (s101_256) already exists
if [ -f "$LOGS_DIR/s101_256/model_final.pth" ]; then
    echo ">>> Trained weights already present at $LOGS_DIR/s101_256/model_final.pth"
else
    echo ""
    echo ">>> Downloading trained Pet-ReID weights from Google Drive..."
    echo "    Source: $GDRIVE_URL"
    echo ""
    gdown --folder "$GDRIVE_URL" --remaining-ok -O "$LOGS_DIR/" || {
        echo ""
        echo "============================================================"
        echo "ERROR: Could not download from Google Drive automatically."
        echo ""
        echo "Please download manually:"
        echo "  1. Open: $GDRIVE_URL"
        echo "  2. Download all .pth files"
        echo "  3. Place them in the following structure:"
        echo "       $LOGS_DIR/s101_224/model_final.pth"
        echo "       $LOGS_DIR/s101_256/model_final.pth  (primary)"
        echo "       $LOGS_DIR/s101_288/model_final.pth"
        echo "       $LOGS_DIR/s200_224/model_final.pth"
        echo ""
        echo "  Or via Baidu Cloud:"
        echo "  https://pan.baidu.com/s/17tnCE8b-oSh8xGMHczPzqQ?pwd=imag"
        echo "============================================================"
        exit 1
    }
fi

echo ""
echo ">>> Verifying weights..."
for model_dir in s101_224 s101_256 s101_288 s200_224; do
    pth="$LOGS_DIR/$model_dir/model_final.pth"
    if [ -f "$pth" ]; then
        size=$(du -h "$pth" | cut -f1)
        echo "    [OK] $model_dir/model_final.pth ($size)"
    else
        echo "    [--] $model_dir/model_final.pth (not found)"
    fi
done

pth="$PRETRAIN_DIR/resnest101-22405ba7.pth"
if [ -f "$pth" ]; then
    size=$(du -h "$pth" | cut -f1)
    echo "    [OK] pretrain/resnest101-22405ba7.pth ($size)"
fi

echo ""
echo ">>> Done. Set ML_MODEL_WEIGHTS env var to use a specific weights file."
echo "    Default: $LOGS_DIR/s101_256/model_final.pth"
