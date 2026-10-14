# This code was made entirely using DeepSeek Coder.
# Link to the model: https://huggingface.co/collections/deepseek-ai/deepseek-coder


import os
from PyInstaller.utils.hooks import collect_dynamic_libs, collect_data_files


binaries = collect_dynamic_libs("llama_cpp") or []
datas = collect_data_files("llama_cpp", include_py_files=False) or []

try:
    import llama_cpp
    lib_dir = os.path.join(os.path.dirname(llama_cpp.__file__), "lib")

    if os.path.isdir(lib_dir):
        for name in os.listdir(lib_dir):
            full = os.path.join(lib_dir, name)

            if not os.path.isfile(full):
                continue

            if name.lower().endswith((".dll", ".so", ".dylib")):
                binaries.append((full, "llama_cpp/lib"))
            elif name.lower().endswith((".metal", ".metallib", ".json")):
                datas.append((full, "llama_cpp/lib"))
except Exception:
    pass