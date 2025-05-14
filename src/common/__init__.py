"""
Common package for SDIMS backend.
"""
import os
import sys
from pathlib import Path

# Add layers/common-layer/python to Python path if not already in sys.path
# This is only needed for local development, not in Lambda environment
REPO_ROOT = Path(__file__).parent.parent.parent  # From src/common to repo root
LAYER_PATH = os.path.join(REPO_ROOT, 'layers', 'common-layer', 'python')

if os.path.exists(LAYER_PATH) and LAYER_PATH not in sys.path:
    sys.path.insert(0, LAYER_PATH)
    print(f"Added {LAYER_PATH} to Python path") 