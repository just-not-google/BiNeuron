from typing import List
from AlexRadar.data.prompt_for_orchestrator_ai_models import PROMPT
from AlexRadar.additional_functions.launching_ai_model_and_requesting import launching_ai_model_and_requesting
import logging


logger = logging.getLogger(__name__)

def orchestrator_ai_models(user_prompt: str,
                           repo_id: str = "Qwen/Qwen2.5-Coder-1.5B-Instruct-GGUF",
                           filename: str = "qwen2.5-coder-1.5b-instruct-q4_k_m.gguf",
                           n_ctx: int = 8192,
                           n_gpu_layers: int = 0,
                           verbose: bool = False,
                           echo: bool = False,
                           models_dir: str = "./models",
                           prefer_mirror: bool = True) -> List[str]:
    """
    Orchestrates AI model to extract programming languages from user prompt.
    :param user_prompt: The user's input text.
    :param repo_id: Hugging Face repository ID for the model.
    :param filename: Model file name.
    :param n_ctx: Context window size.
    :param n_gpu_layers: Number of GPU layers.
    :param verbose: Whether to enable verbose output.
    :param echo: Whether to echo input.
    :param models_dir: Directory to cache downloaded models.
    :param prefer_mirror: If True, forces using the mirror endpoint (hf-mirror.com).
    :return: List of programming language names extracted from the prompt.
    """
    logger.info("Challenge orchestrator_ai_models")
    try:
        ai_answer = launching_ai_model_and_requesting(
            messages=user_prompt,
            repo_id=repo_id,
            filename=filename,
            n_ctx=n_ctx,
            n_gpu_layers=n_gpu_layers,
            template_prompt=PROMPT,
            verbose=verbose,
            echo=echo,
            models_dir=models_dir,
            prefer_mirror=prefer_mirror
        )

        logger.info("The main programming languages have been identified from your request thanks to AI")
        return ai_answer.strip().split(" ")

    except Exception as e:
        logger.exception(f"Error when trying to get programming languages from your request via AI - {e}")
        return []