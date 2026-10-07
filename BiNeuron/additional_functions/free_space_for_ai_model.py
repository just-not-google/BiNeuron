from huggingface_hub import HfApi
from typing import Optional
import shutil
import logging


logger = logging.getLogger(__name__)

def get_file_size(
        repo_id: str,
        filename: str,
        attempts: int
) -> Optional[int]:
    """
    Determining the weight of an AI model with Hugging Face.
    :param repo_id: Explicit Hugging Face repository ID.
    :param filename: Filename of the model inside the repository.
    :param attempts: The number of attempts to get the data.
    :return: The final integer is purely in bytes.
    """
    logger.info("Challenge get_file_size")
    for _ in range(attempts):
        try:
            api = HfApi()
            info = api.get_paths_info(
                repo_id=repo_id,
                paths=[filename],
                repo_type="model"
            )
            logger.info("The total weight of the AI model is obtained.")
            return info[0].size
        except Exception as e:
            logger.exception(f"Error when trying to get data on the weight of the AI model - {e}")
            continue
    return None

def free_disk_space(path: Optional[str], attempts: int) -> Optional[int]:
    """
    Determining the free space on the user's disk.
    :param path: The path to the disk being checked.
    :param attempts: The number of attempts to get the data.
    :return: The final integer is purely in bytes.
    """
    logger.info("Challenge free_disk_space")
    for _ in range(attempts):
        try:
            usage = shutil.disk_usage(path=path)
            logger.info("A free disk space value was received.")
            return usage.free
        except Exception as e:
            logger.exception(f"Error when trying to get data about free disk space - {e}")
            continue
    return None

def free_space_for_ai_model(
        repo_id: str,
        filename: str,
        attempts: int,
        path: Optional[str]
) -> bool:
    """
    Checks the condition that there is enough space
    for the AI model on the user's disk.
    :param repo_id: Explicit Hugging Face repository ID.
    :param filename: Filename of the model inside the repository.
    :param attempts: The number of attempts to get the data.
    :param path: The path to the disk being checked.
    :return: True if the disk space is more than the AI
    model weighs, otherwise False.
    """
    logger.info("Challenge free_space_for_ai_model")
    model_weight = get_file_size(
        repo_id=repo_id,
        filename=filename,
        attempts=attempts
    )
    weight_free_disk = free_disk_space(
        path=path,
        attempts=attempts
    )

    if model_weight is None or weight_free_disk is None:
        logger.info("The data is incomplete for comparison, and the verification cannot be continued.")
        return False

    if model_weight > weight_free_disk:
        logger.info("The disk space is less than the weight of the model, the download cannot start.")
        return False

    logger.warning("The disk space allows you to download this AI model.")
    return True
