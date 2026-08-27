from deepseek_ocr import DeepSeekOCR as CloudDeepSeek
import logging
from typing import Literal, Optional
import random
from AlexRadar.data.constants_for_functions import (MIN_TIMEOUT_FOR_CHECK, MAX_TIMEOUT_FOR_CHECK,
                                                    NUMBER_ATTEMPTS, TINY_TYPE, DEVICE_OPTIONS,
                                                    RETURN_TENSORS, MAX_NEW_TOKENS, DEEPSEEK_LOCAL_OCR)
from AlexRadar.additional_functions.checking_integer_for_condition import checking_int_and_float
import torch
from transformers import AutoProcessor, AutoModelForImageTextToText
from PIL import Image
from AlexRadar.data.prompt_for_ocr import PROMPT
from AlexRadar.data.model_repo_map import MODEL_REPO_MAP


logger = logging.getLogger(__name__)

class LaunchDeepSeekOCR:
    def __init__(self,
                 photo_path: str,
                 cloud_version: bool = False,
                 model_size: Literal["tiny", "small", "base", "large", "gundam"] = TINY_TYPE,
                 device: Literal["cpu", "cuda:0"] = DEVICE_OPTIONS[0],
                 crop_mode: bool = False,
                 base_url: str = "https://api.siliconflow.cn/v1/chat/completions",
                 api_key_for_deepseek_ocr: Optional[str] = None,
                 timeout_for_deepseek_ocr: Optional[int] = None,
                 max_rate_limit_retries: Optional[int] = NUMBER_ATTEMPTS) -> None:
        """
        Initialization of the photo text detection launcher using the DeepSeek AI model.
        :param photo_path: The path to the photo that is being determined.
        :param cloud_version: Whether to use the API is False by default.
        :param model_size: The size and accuracy of the model.
        :param device: Running on a processor or on a graphics card.
        :param crop_mode: Splits large images into several fragments for more detailed recognition.
        :param base_url: The API link to which the request will be sent.
        :param api_key_for_deepseek_ocr: The key for the API to work.
        :param timeout_for_deepseek_ocr: The time of the API request.
        :param max_rate_limit_retries: The number of API request attempts.
        """
        logger.info("Initializing LaunchDeepSeekOCR")
        self.photo_path = photo_path
        self.cloud_version = cloud_version
        self.local_settings = {
            "model_size": model_size,
            "device": device,
            "crop_mode": crop_mode
        }
        self.local_model_repo = MODEL_REPO_MAP.get(model_size, DEEPSEEK_LOCAL_OCR)
        self.local_model = None
        self.local_processor = None

        if not checking_int_and_float(timeout_for_deepseek_ocr):
            timeout_for_deepseek_ocr = None

        if not checking_int_and_float(max_rate_limit_retries):
            max_rate_limit_retries = NUMBER_ATTEMPTS

        if timeout_for_deepseek_ocr is None:
            timeout_for_deepseek_ocr = random.randint(MIN_TIMEOUT_FOR_CHECK,
                                                      MAX_TIMEOUT_FOR_CHECK)

        self.cloud_settings = {
            "base_url": base_url,
            "api_key_for_deepseek_ocr": api_key_for_deepseek_ocr,
            "timeout_for_deepseek_ocr": timeout_for_deepseek_ocr,
            "enable_rate_limit_retry": True,
            "max_rate_limit_retries": max_rate_limit_retries
        }

    def _load_local_model(self):
        """
        Loads the model and processor with Hugging Face (cached in self.local_model).
        """
        logger.info("Challenge _load_local_model")
        if self.local_model is None:
            device = self.local_settings["device"]
            dtype = torch.float16 if device == "cuda:0" else torch.float32
            logger.info(f"Loading the local model {self.local_model_repo}.")
            self.local_processor = AutoProcessor.from_pretrained(self.local_model_repo, trust_remote_code=True)
            self.local_model = AutoModelForImageTextToText.from_pretrained(
                self.local_model_repo,
                torch_dtype=dtype,
                trust_remote_code=True
            )
            self.local_model.to(device)
            logger.info("The local model is loaded.")
        return self.local_model, self.local_processor

    def _local_deepseek_ocr(self) -> Optional[str]:
        """
        Local launch of DeepSeek OCR via Transformers.
        """
        logger.info("Challenge _local_deepseek_ocr")
        try:
            model, processor = self._load_local_model()
            device = self.local_settings["device"]
            crop_mode = self.local_settings["crop_mode"]
            image = Image.open(self.photo_path).convert("RGB")

            if crop_mode:
                width, height = image.size
                crops = [
                    (0, 0, width // 2, height // 2),
                    (width // 2, 0, width, height // 2),
                    (0, height // 2, width // 2, height),
                    (width // 2, height // 2, width, height)
                ]
                texts = []
                for box in crops:
                    crop = image.crop(box)
                    inputs = processor(images=crop, text=PROMPT, return_tensors=RETURN_TENSORS).to(device)
                    outputs = model.generate(**inputs, max_new_tokens=MAX_NEW_TOKENS)
                    text = processor.decode(outputs[0], skip_special_tokens=True)
                    texts.append(text)
                result = "\n".join(texts)
            else:
                inputs = processor(images=image, text=PROMPT, return_tensors=RETURN_TENSORS).to(device)
                outputs = model.generate(**inputs, max_new_tokens=MAX_NEW_TOKENS)
                result = processor.decode(outputs[0], skip_special_tokens=True)

            logger.info("The text from the photo was received via a local launch.")
            return result.strip()
        except Exception as e:
            logger.exception(f"Error when trying to get text from a photo locally - {e}")
            return None

    def _cloud_deepseek_ocr(self) -> Optional[str]:
        """
        Cloud launch of the model and subsequent access to it via the API.
        """
        logger.info("Challenge _cloud_deepseek_ocr")
        try:
            client = CloudDeepSeek(**self.cloud_settings)
            result = client.parse(file_path=self.photo_path)

            logger.info("The text from the photo was received via a cloud launch.")
            return result
        except Exception as e:
            logger.exception(f"Error when trying to cloud text from a photo - {e}")
            return None

    def advanced_definition_text_from_image(self) -> str:
        """
        The main function that determines which type of processing to
        choose when accessing the 'cloud_version' parameter.
        """
        logger.info("Challenge advanced_definition_text_from_image")
        answer = None

        if self.cloud_version:
            logger.info("The cloud version is selected.")
            answer = self._cloud_deepseek_ocr()
        else:
            logger.info("The local version is selected.")
            answer = self._local_deepseek_ocr()

        if answer is None:
            logger.warning("None of the methods could get the text from this photo.")
            return "The program couldn't read the text from the photo."
        return answer