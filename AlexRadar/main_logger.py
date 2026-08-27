import logging
import sys

root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s', datefmt='%H:%M:%S')
console_handler.setFormatter(console_formatter)
root_logger.addHandler(console_handler)

file_handler = logging.FileHandler('errors.log', encoding='utf-8')
file_handler.setLevel(logging.ERROR)
file_formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(module)s:%(lineno)d - %(message)s')
file_handler.setFormatter(file_formatter)
root_logger.addHandler(file_handler)