from BiNeuron.data.prompt_for_compression import PROMPT_FOR_COMPRESSION
from BiNeuron.additional_functions.template_for_changing_text_query_via_ai import template_for_changing_text_query_via_ai
from BiNeuron.data.constants_for_functions import (
    MAIN_REPO_ID, MAIN_FILENAME, MAX_TOKENS_LITE, MODELS_DIR_CONST
)
import logging


logger = logging.getLogger(__name__)

def logic_text_compression(
        original_text: str,
        models_dir: str = MODELS_DIR_CONST,
        n_gpu_layers: int = 0,
        verbose: bool = False,
        prefer_mirror: bool = True,
        repo_id: str = MAIN_REPO_ID,
        filename: str = MAIN_FILENAME,
        max_tokens: int = MAX_TOKENS_LITE
) -> str:
    """
    Compresses text using the same small local model (Qwen).
    Falls back to the original text if compression fails.
    :param original_text: The text that will be compressed.
    :param models_dir: Directory where downloaded models are cached.
    :param n_gpu_layers: Number of GPU layers to offload. 0 means CPU-only.
    :param verbose: Enables verbose output from the underlying LLM.
    :param prefer_mirror: If True, forces using the mirror endpoint (hf-mirror.com).
    :param repo_id: Explicit Hugging Face repository ID.
    :param filename: Filename of the model inside the repository.
    :param max_tokens: Maximum tokens to generate.
    :return: Compressed text as a string.
    """
    logger.info("Challenge logic_text_compression")
    temp_late = template_for_changing_text_query_via_ai(
        original_text=original_text,
        template_prompt=PROMPT_FOR_COMPRESSION,
        models_dir=models_dir,
        n_gpu_layers=n_gpu_layers,
        verbose=verbose,
        prefer_mirror=prefer_mirror,
        repo_id=repo_id,
        filename=filename,
        max_tokens=max_tokens,
        text_for_logger=[
            "The compressed text turned out to be empty, and the original text was returned.",
            "An abbreviated general text was received.",
            "An error occurred when trying to compress the text"
        ]
    )
    return temp_late