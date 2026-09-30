import os
import sys
from pathlib import Path

import torch

sys.path.append(str(Path(__file__).resolve().parents[1]))


def main():
    print("Python:", sys.version)
    print("PyTorch:", torch.__version__)
    print("CUDA available:", torch.cuda.is_available())
    print("MPS built:", torch.backends.mps.is_built())
    print("MPS available:", torch.backends.mps.is_available())
    print("HF_HOME:", os.environ.get("HF_HOME"))
    print("HF_HUB_CACHE:", os.environ.get("HF_HUB_CACHE"))
    if torch.cuda.is_available():
        print("Selected device: cuda")
    elif torch.backends.mps.is_available():
        print("Selected device: mps")
    else:
        print("Selected device: cpu")

if __name__ == "__main__":
    main()
