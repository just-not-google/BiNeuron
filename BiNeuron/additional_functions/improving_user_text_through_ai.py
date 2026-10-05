from BiNeuron.data.prompt_for_improvement import PROMPT_FOR_IMPROVEMENT
from BiNeuron.additional_functions.template_for_changing_text_query_via_ai import template_for_changing_text_query_via_ai
from BiNeuron.data.constants_for_functions import (MAIN_REPO_ID, MAIN_FILENAME, MAX_TOKENS_LITE,
                                                   MODELS_DIR_CONST)
import logging


logger = logging.getLogger(__name__)

def improving_user_text_through_ai(original_text: str,
                                   models_dir: str = MODELS_DIR_CONST,
                                   n_gpu_layers: int = 0,
                                   verbose: bool = False,
                                   prefer_mirror: bool = True,
                                   repo_id: str = MAIN_REPO_ID,
                                   filename: str = MAIN_FILENAME,
                                   max_tokens: int = MAX_TOKENS_LITE) -> str:
    """
    Rewrites the user's raw request into a clear, structured, and well-formed prompt.
    Applies PROMPT_FOR_IMPROVEMENT to the original text via a local small model
    (Qwen by default). The result preserves the original meaning, language, and
    all technical details (file names, function names, error messages, code).
    If the model returns an empty result or an error occurs, the original text
    is returned unchanged.
    :param original_text: The user's raw request that needs to be improved.
    :param models_dir: Directory where downloaded models are cached.
    :param n_gpu_layers: Number of GPU layers to offload. 0 means CPU-only.
    :param verbose: Enables verbose output from the underlying LLM.
    :param prefer_mirror: If True, forces using the mirror endpoint (hf-mirror.com).
    :param repo_id: Explicit Hugging Face repository ID.
    :param filename: Filename of the model inside the repository.
    :param max_tokens: Maximum number of tokens to generate.
    :return: Improved and structured request text, or the original text if
    improvement failed or returned empty.
    """
    logger.info("Challenge improving_user_text_through_ai")
    temp_late = template_for_changing_text_query_via_ai(
        original_text=original_text,
        template_prompt=PROMPT_FOR_IMPROVEMENT,
        models_dir=models_dir,
        n_gpu_layers=n_gpu_layers,
        verbose=verbose,
        prefer_mirror=prefer_mirror,
        repo_id=repo_id,
        filename=filename,
        max_tokens=max_tokens,
        text_for_logger=[
            "Even after the improvement, the text remained blank, so the original text will be returned.",
            "A more structured and improved text was obtained through AI.",
            "Error when trying to make it more structured and understandable"
        ]
    )
    return temp_late