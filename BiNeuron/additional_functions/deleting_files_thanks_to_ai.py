import os
import logging


logger = logging.getLogger(__name__)

def deleting_files_thanks_to_ai(answer_json: dict) -> None:
    """
    Deleting a file if it is None in the JSON response from AI.
    :param answer_json: Dictionary where keys are file paths and
    values are new contents (or None for deletion).
    :return: It does not return anything, but only deletes it.
    """
    logger.info("Challenge deleting_files_thanks_to_ai")
    for key, value in answer_json.items():
        if value is None:
            if not os.path.exists(key):
                logger.warning(f"{key} - the file was not found using this path.")
                continue

            os.remove(key)
    logger.info("The file deletion process has been completed completely.")