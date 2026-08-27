import logging


logger = logging.getLogger(__name__)

def checking_int_and_float(value: int or float,
                           option_1: bool = True) -> bool:
    """
    Checking integers and floating-point numbers for validity.
    :param value: The number itself is for verification.
    :param option_1: Support for multiple number variants.
    :return: A Boolean value. True if all checks are successful, otherwise False
    """
    logger.info("Challenge checking_int_and_float")
    if option_1:
        if not isinstance(value, int):
            logger.warning("Error because the passed value is not an integer.")
            return False
    else:
        if not isinstance(value, float):
            logger.warning("Error because the passed value is not an float.")
            return False

    if value < 0:
        logger.warning("Error because the passed value is less than zero (negative).")
        return False

    return True