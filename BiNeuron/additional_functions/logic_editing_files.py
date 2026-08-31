import json
from pathlib import Path
from typing import Optional
from BiNeuron.data.supported_formats_and_writemode import SUPPORTED_FORMATS_W, SUPPORTED_FORMATS_WB
import logging


logger = logging.getLogger(__name__)

def logic_editing_files(str_json: str) -> Optional[bool]:
    """
    The AI response is converted into a JSON object and then files are overwritten or created that are
    specified in the keys of this json, with the value specified in the same JSON. The suffix defines
    a record in text or bytes.
    :param str_json: The AI's response is in the form of a JSON file.
    :return: If there is an error reading the JSON file, a Boolean value is returned, otherwise None.
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
            suffix = Path(key).suffix.lower()

            if suffix in SUPPORTED_FORMATS_W:
                with open(key, "w", encoding="utf-8") as file:
                    file.write(value)
            elif suffix in SUPPORTED_FORMATS_WB:
                with open(key, "wb", encoding="utf-8") as file:
                    file.write(value.encode("utf-8"))
        except Exception as e:
            logger.exception(f"An error occurred when trying to edit the file ({key}) - {e}")
            continue
    logger.info(f"All the necessary files have been changed.")