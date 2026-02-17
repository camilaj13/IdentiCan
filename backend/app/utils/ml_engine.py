"""
Pet-ReID-IMAG integration for dog nose biometric identification.

Uses the fastreid-based Pet-ReID model to extract 2048-dimensional
embeddings from nose images and compute cosine similarity for matching.
"""

import logging
import os
import sys
from io import BytesIO
from pathlib import Path
from typing import List, Optional, Tuple

import numpy as np
from PIL import Image

logger = logging.getLogger(__name__)

# Path to the ml_model directory (sibling of backend/)
ML_MODEL_DIR = Path(__file__).resolve().parents[3] / "ml_model"

# Lazy-loaded globals
_model = None
_cfg = None
_torch = None


def _get_torch():
    """Lazy import torch to avoid import cost when not needed (e.g. tests)."""
    global _torch
    if _torch is None:
        import torch
        _torch = torch
    return _torch


def _load_model():
    """
    Build and return the Pet-ReID model.

    Loads the fastreid Baseline architecture with ResNeSt-101 backbone.
    If trained weights (MODEL_WEIGHTS env var or default path) exist,
    loads them. Otherwise uses randomly-initialized weights (the model
    still functions as a feature extractor).
    """
    global _model, _cfg

    if _model is not None:
        return _model, _cfg

    torch = _get_torch()

    # Add ml_model to path so fastreid imports work
    ml_model_str = str(ML_MODEL_DIR)
    if ml_model_str not in sys.path:
        sys.path.insert(0, ml_model_str)

    from fastreid.config import get_cfg
    from fastreid.modeling.meta_arch import build_model
    from fastreid.utils.checkpoint import Checkpointer
    from pet_id.config import add_retri_config

    cfg = get_cfg()
    add_retri_config(cfg)

    config_file = str(ML_MODEL_DIR / "configs" / "s101_256_submit.yaml")
    cfg.merge_from_file(config_file)

    cfg.defrost()
    cfg.MODEL.DEVICE = "cpu"
    cfg.MODEL.BACKBONE.PRETRAIN = False
    cfg.MODEL.HEADS.NUM_CLASSES = 1
    cfg.freeze()

    model = build_model(cfg)
    model.eval()

    # Try to load trained weights
    weights_path = os.environ.get("ML_MODEL_WEIGHTS", "")
    if not weights_path:
        # Check default location
        default_path = ML_MODEL_DIR / "logs" / "s101_256" / "model_final.pth"
        if default_path.exists():
            weights_path = str(default_path)

    if weights_path and os.path.isfile(weights_path):
        logger.info("Loading Pet-ReID weights from %s", weights_path)
        Checkpointer(model).load(weights_path)
    else:
        logger.warning(
            "No trained Pet-ReID weights found. "
            "Model will use untrained weights. "
            "Set ML_MODEL_WEIGHTS env var to the path of model_final.pth."
        )

    _model = model
    _cfg = cfg
    logger.info("Pet-ReID model loaded (backbone=ResNeSt-101, embedding_dim=2048)")
    return _model, _cfg


def extract_embedding(image_bytes: bytes) -> List[float]:
    """
    Extract a 2048-dimensional embedding from a nose image.

    Args:
        image_bytes: Raw bytes of the image (JPEG, PNG, etc.)

    Returns:
        List of 2048 floats representing the nose embedding.
    """
    torch = _get_torch()
    model, cfg = _load_model()

    img = Image.open(BytesIO(image_bytes)).convert("RGB")

    # Resize to model input size
    size = cfg.INPUT.SIZE_TEST  # [H, W] = [256, 256]
    img = img.resize((size[1], size[0]), Image.BILINEAR)

    img_array = np.array(img, dtype=np.float32)  # (H, W, 3)
    img_tensor = torch.from_numpy(img_array).permute(2, 0, 1).unsqueeze(0)  # (1, 3, H, W)

    with torch.no_grad():
        embedding = model({"images": img_tensor})  # (1, 2048)

    return embedding[0].tolist()


def extract_embedding_multi(images_bytes: List[bytes]) -> List[float]:
    """
    Extract an averaged embedding from multiple nose images.

    Computes an embedding for each image and returns the L2-normalized
    mean embedding. This gives a more robust representation than a
    single image.

    Args:
        images_bytes: List of raw image bytes.

    Returns:
        List of 2048 floats (averaged, normalized embedding).
    """
    if not images_bytes:
        raise ValueError("At least one image is required")

    embeddings = [extract_embedding(img) for img in images_bytes]

    arr = np.array(embeddings, dtype=np.float32)  # (N, 2048)
    mean_emb = arr.mean(axis=0)  # (2048,)

    # L2 normalize
    norm = np.linalg.norm(mean_emb)
    if norm > 0:
        mean_emb = mean_emb / norm

    return mean_emb.tolist()


def compute_similarity(embedding_a: List[float], embedding_b: List[float]) -> float:
    """
    Compute cosine similarity between two embeddings.

    Args:
        embedding_a: First embedding (list of floats).
        embedding_b: Second embedding (list of floats).

    Returns:
        Float in [-1, 1]. Higher = more similar.
    """
    a = np.array(embedding_a, dtype=np.float32)
    b = np.array(embedding_b, dtype=np.float32)

    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return float(np.dot(a / norm_a, b / norm_b))


def find_best_match(
    query_embedding: List[float],
    gallery: List[Tuple[int, List[float]]],
    threshold: float = 0.5,
) -> Optional[Tuple[int, float]]:
    """
    Find the best matching dog from a gallery of stored embeddings.

    Args:
        query_embedding: The embedding of the query nose image.
        gallery: List of (dog_id, embedding) tuples.
        threshold: Minimum cosine similarity to consider a match.

    Returns:
        (dog_id, similarity) of the best match, or None if no match
        exceeds the threshold.
    """
    if not gallery:
        return None

    best_id = None
    best_sim = -1.0

    for dog_id, stored_emb in gallery:
        sim = compute_similarity(query_embedding, stored_emb)
        if sim > best_sim:
            best_sim = sim
            best_id = dog_id

    if best_sim >= threshold:
        return (best_id, best_sim)

    return None
