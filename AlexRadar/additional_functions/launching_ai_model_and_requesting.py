from typing import Optional, List, Dict, Union
from llama_cpp import Llama
from AlexRadar.additional_functions.checking_and_downloading_ai_model import ModelDownloader
from AlexRadar.additional_functions.checking_integer_for_condition import checking_int_and_float
from AlexRadar.data.constants_for_functions import MAX_TOKENS_LITE
import logging


logger = logging.getLogger(__name__)

def launching_ai_model_and_requesting(messages: Union[str, List[Dict[str, str]]],
                                      repo_id: str,
                                      filename: str,
                                      models_dir: str,
                                      template_prompt: str = "",
                                      n_ctx: Optional[int] = None,
                                      n_gpu_layers: int = 0,
                                      verbose: bool = False,
                                      echo: bool = False,
                                      max_tokens: int = MAX_TOKENS_LITE,
                                      temperature: float = 0.1,
                                      llm: Optional[Llama] = None,
                                      prefer_mirror: bool = True) -> str:
    """
    Loads an AI model and sends a request with given messages.
    :param messages: Input text (string) or chat messages (list of dicts).
    :param repo_id: Hugging Face repository ID.
    :param filename: Model file name.
    :param models_dir: Directory to cache downloaded models.
    :param template_prompt: Template string with '{your_prompt_for_ai}' placeholder (for string messages).
    :param n_ctx: Context length for the model.
    :param n_gpu_layers: Number of GPU layers.
    :param verbose: Enable verbose logging.
    :param echo: Echo the prompt in output (for string mode).
    :param max_tokens: Maximum tokens to generate.
    :param temperature: Sampling temperature.
    :param llm: Existing Llama instance; if None, loads a new one.
    :param prefer_mirror: If True, forces using the mirror endpoint (hf-mirror.com).
    :return: Generated text response or error message.
    """
    logger.info("Challenge launching_ai_model_and_requesting")
    try:
        if not checking_int_and_float(n_ctx):
            n_ctx = None
        if not checking_int_and_float(n_gpu_layers):
            n_gpu_layers = 0
        if not checking_int_and_float(max_tokens):
            max_tokens = MAX_TOKENS_LITE
        if not checking_int_and_float(temperature, option_1=False):
            temperature = 0.1

        if llm is None:
            model_downloader = ModelDownloader(repo_id=repo_id,
                                               filename=filename,
                                               prefer_mirror=prefer_mirror)
            model_downloader.auto_manager_for_download()

            llm = Llama.from_pretrained(
                repo_id=repo_id,
                filename=filename,
                n_ctx=n_ctx,
                n_gpu_layers=n_gpu_layers,
                verbose=verbose,
                cache_dir=models_dir
            )
            logger.info("The model is loaded into memory.")

        if isinstance(messages, str):
            prompt = template_prompt.replace("{your_prompt_for_ai}", messages)
            output = llm(
                prompt,
                max_tokens=max_tokens,
                temperature=temperature,
                echo=echo
            )
            answer_text = output["choices"][0]["text"]
            logger.info("Response received (old mode with template).")
        elif isinstance(messages, list):
            output = llm.create_chat_completion(
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
            )
            answer_text = output["choices"][0]["message"]["content"]
            logger.info("Response received (chat mode).")
        else:
            raise ValueError("'messages' must be a string or a list of dictionaries.")

        return answer_text

    except Exception as e:
        logger.exception(f"Error accessing the local model - {e}")
        return f"Error - {e}"