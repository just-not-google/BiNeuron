# This code was made entirely using DeepSeek Coder.
# Link to the model: https://huggingface.co/collections/deepseek-ai/deepseek-coder


import os
import sys

if getattr(sys, "frozen", False):
    bundle_dir = getattr(sys, "_MEIPASS", os.path.dirname(sys.executable))

    candidates = [
        os.path.join(bundle_dir, "llama_cpp", "lib"),
        os.path.join(bundle_dir, "llama_cpp"),
    ]

    for path in candidates:
        if not os.path.isdir(path):
            continue

        if hasattr(os, "add_dll_directory"):
            try:
                os.add_dll_directory(path)
            except OSError:
                pass

        os.environ["PATH"] = path + os.pathsep + os.environ.get("PATH", "")