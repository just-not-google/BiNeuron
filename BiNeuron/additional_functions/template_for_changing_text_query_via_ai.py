from BiNeuron.additional_functions.launching_ai_model_and_requesting import launching_ai_model_and_requesting
from typing import List, Optional
import logging


logger = logging.getLogger(__name__)

def template_for_changing_text_query_via_ai(original_text: str,
                                            template_prompt: str,
                                            text_for_logger: Optional[List[str]],
                                            models_dir: str,
                                            n_gpu_layers: int,
                                            verbose: bool,
                                            prefer_mirror: bool,
                                            repo_id: str,
                                            filename: str,
                                            max_tokens: int) -> str:
    """
    Universal template for sending a text-transformation request to a local AI model.
    Used by any function that needs to modify, rewrite, compress, or restructure
    the user's text through an LLM. Applies the given template prompt, sends the
    original text to the model, and returns the transformed result. If the model
    returns an empty response or an error occurs, the original text is returned
    unchanged.
    :param original_text: The source text to be transformed by the AI.
    :param template_prompt: Template string containing the '{your_prompt_for_ai}'
    placeholder, into which the original text will be inserted.
    :param text_for_logger: Messages for passing the function.
    :param models_dir: Directory where downloaded models are cached.
    :param n_gpu_layers: Number of GPU layers to offload. 0 means CPU-only.
    :param verbose: Enables verbose output from the underlying LLM.
    :param prefer_mirror: If True, forces using the mirror endpoint (hf-mirror.com).
    :param repo_id: Explicit Hugging Face repository ID.
    :param filename: Filename of the model inside the repository.
    :param max_tokens: Maximum number of tokens to generate.
    :return: Transformed text as a string, or the original text if transformation
    failed or returned empty.
    """
    logger.info(f"Challenge template_for_changing_text_query_via_ai")

    if not original_text or not original_text.strip():
        return original_text

    try:

        improved_text = launching_ai_model_and_requesting(
            messages=original_text,
            repo_id=repo_id,
            filename=filename,
            n_gpu_layers=n_gpu_layers,
            verbose=verbose,
            models_dir=models_dir,
            prefer_mirror=prefer_mirror,
            template_prompt=template_prompt,
            max_tokens=max_tokens,
        )

        if not improved_text or not improved_text.strip():
            logger.warning(text_for_logger[0])
            return original_text

        logger.info(text_for_logger[1])
        return improved_text.strip()

    except Exception as e:
        logger.exception(f"{text_for_logger[2]} - {e}")
        return original_text