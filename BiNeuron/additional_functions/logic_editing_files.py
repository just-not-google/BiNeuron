import json
from pathlib import Path
from typing import Optional, Union, Dict
from BiNeuron.data.supported_formats_and_writemode import SUPPORTED_FORMATS_W
import logging


logger = logging.getLogger(__name__)

def logic_editing_files(str_json: str) -> Union[Optional[bool], Optional[Dict]]:
    """
    Apply file changes described in a JSON object produced by the AI.
    The function parses the input string as JSON, where each key is an absolute
    file path and each value is the complete new content for that file. For each
    entry, the file is created or overwritten with the provided content. Only
    text-based formats listed in SUPPORTED_FORMATS_W are processed; binary
    formats (PDF, DOCX, PPTX, images, etc.) are skipped with a warning, since
    they cannot be safely reconstructed from a text value. Entries with a
    `null` value are ignored (deletion is handled elsewhere, if enabled).
    :param str_json: JSON string where keys are file paths and values are new file contents.
    :return: Parsed JSON dictionary on success, or False if the input is not valid JSON.
    """
    logger.info("Challenge logic_editing_files")
    answer_json = None
    try:
        answer_json = json.loads(str_json)
    except Exception as e:
        logger.exception(f"An error occurred while trying to format a JSON file - {e}")
        return False

    logger.info("The beginning of the process of creating and modifying files using a JSON file.")
    for key, value in answer_json.items():
        try:
            if value is None:
                continue

            suffix = Path(key).suffix.lower()

            if suffix in SUPPORTED_FORMATS_W:
                with open(key, "w", encoding="utf-8") as file:
                    file.write(value)
            else:
                logger.warning(f"Skipping binary file: {key} (not editable via JSON).")
        except Exception as e:
            logger.exception(f"An error occurred when trying to edit the file ({key}) - {e}")
            continue
    logger.info(f"All the necessary files have been changed.")
    return answer_json