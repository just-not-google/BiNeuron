import click
from AlexRadar.main import AlexRadar
import AlexRadar.main_logger
from typing import Optional
from AlexRadar.data import TYPE_DEFAULT
from AlexRadar.data.preferences_in_ai import PreferenceInAI
from AlexRadar.data.constants_for_functions import (HTTP_PROTOCOL, MAX_TIMEOUT, MAX_TOKENS,
                                                    MIN_TIMEOUT_FOR_CHECK, MAX_TIMEOUT_FOR_CHECK,
                                                    MAIN_LANGUAGE, NUMBER_ATTEMPTS, MAIN_PROXY_ATTEMPTS,
                                                    TINY_TYPE)


@click.command()
@click.argument("request", required=True)
@click.option("--preferences_in_ai", "-p",
              type=click.Choice([e.value for e in PreferenceInAI], case_sensitive=True),
              default=PreferenceInAI.DEEPSEEK.value,
              help="The model for multilingual queries (by default).")
@click.option("--filter_for_swearing", "-fs",
              is_flag=True,
              help="Block requests with profanity.")
@click.option("--additional_files", "-af",
              multiple=True,
              type=click.Path(exists=True, readable=True, dir_okay=False),
              help="Additional files for the context (you can specify several).")
@click.option("--models_dir", "-md",
              default="./models",
              help="Folder for downloading local models.")
@click.option("--with_ai_orchestrator", "-wor",
              is_flag=True,
              default=True,
              help="Use AI to identify programming languages.")
@click.option("--verbose", "-v",
              is_flag=True,
              help="Display technical information.")
@click.option("--n_ctx", "-nc",
              type=int,
              default=None,
              help="The size of the context window (None = auto-detection).")
@click.option("--n_gpu_layers", "-ng",
              type=int,
              default=0,
              help="The number of layers in the GPU (0 = CPU only).")
@click.option("--echo", "-ec",
              is_flag=True,
              help="Duplicate the request in the AI response.")
@click.option("--max_tokens", "-mt",
              type=int,
              default=MAX_TOKENS,
              help="The maximum response length in tokens.")
@click.option("--your_token_for_hf", "-yt",
              default="",
              help="Hugging Face token to speed up the download.")
@click.option("--subdomain", "-s",
              default="",
              help="A subdomain for uploading the model (if required).")
@click.option("--country", "-c",
              default=None,
              help="The country to select the proxy (for example, ru).")
@click.option("--protocol", "-pr",
              default=HTTP_PROTOCOL,
              help="The protocol for uploading (http/https).")
@click.option("--max_timeout", "-mtm",
              type=int,
              default=MAX_TIMEOUT,
              help="The timeout for loading the model via the proxy (in seconds).")
@click.option("--is_working", "-isw",
              is_flag=True,
              default=True,
              help="Use only working proxies.")
@click.option("--type_computer", "-tc",
              default=None,
              help="Computer type (auto, power, medium, weak) to select the model.")
@click.option("--auto_proxies", "-ap",
              is_flag=True,
              default=True,
              help="Automatically detect whether a proxy is needed to access HF.")
@click.option("--writing_response_to_file", "-wr",
              is_flag=True,
              default=False,
              help="Save the AI response to a file.")
@click.option("--your_proxies_dict", "-ypd",
              multiple=True,
              help="List of proxy URLs (can be specified multiple times).")
@click.option("--determinant_mode", "-dm",
              type=click.Choice(["lite", "full", "auto"]),
              default="lite",
              help="Mode for determinant (lite/full/auto).")
@click.option("--accurate_translation", "-at",
              is_flag=True,
              default=False,
              help="Using a more accurate text translator for better understanding by the AI model (DeepL).")
@click.option("--your_key_for_deepl", "-ykd",
              default="",
              help="The key for accessing the DeepL Translator API.")
@click.option("--proprietary_algorithms", "-pa",
              is_flag=True,
              default=False,
              help="Using internal programming language detection algorithms or using ready-made libraries.")
@click.option("--repo_id", "-ri",
              default=None,
              help="The name of the repository of the AI model is filled in automatically by default.")
@click.option("--filename", "-f",
              default=None,
              help="The name of the model itself from the repository. By default, automatic selection.")
@click.option("--min_timeout_for_checking_availability", "-mint",
              type=int,
              default=MIN_TIMEOUT_FOR_CHECK,
              help="Time to check the availability of the service for downloading models (Minimum).")
@click.option("--max_timeout_for_checking_availability", "-maxt",
              type=int,
              default=MAX_TIMEOUT_FOR_CHECK,
              help="Time to check the availability of the service for downloading models (Maximum).")
@click.option("--request_language", "-rl",
              default=MAIN_LANGUAGE,
              help="The language to translate the request into. English is the default, and the models have a better code.")
@click.option("--main_prompt_mode", "-mpm",
              type=click.Choice(["default", "testing", "explanation", "no_comments", "refactor",
                                 "debug", "code_review", "documentation", "scaffold", "security_hardening",
                                 "algorithm_strategy"]),
              default=TYPE_DEFAULT,
              help="Select the main prompt from the ready dictionary.")
@click.option("--main_prompt", "-mp",
              default=None,
              help="Your own main prompt for AI.")
@click.option("--temperature", "-t",
              type=float,
              default=0.1,
              help="Sampling temperature for the AI response (0.0 to 1.0).")
@click.option("--retries", "-r",
              type=int,
              default=NUMBER_ATTEMPTS,
              help="The number of attempts to download a model using a proxy from the Hugging Face service.")
@click.option("--github_proxies", "-gp",
              is_flag=True,
              default=False,
              help="If True, attempt to fetch proxies from GitHub raw lists first.")
@click.option("--url_lst", "-ul",
              multiple=True,
              default=None,
              help="List of raw GitHub URLs containing proxy lists.")
@click.option("--proxy_retries", "-prt",
              type=int,
              default=NUMBER_ATTEMPTS,
              help="Number of attempts per URL when fetching from GitHub.")
@click.option("--main_retries", "-mrt",
              type=int,
              default=MAIN_PROXY_ATTEMPTS,
              help="Number of times to retry obtaining a working proxy from GitHub.")
@click.option("--lang_lst", "-ll",
              multiple=True,
              type=str,
              default=None,
              help="List of programming languages to consider (optional).")
@click.option("--use_gpu_for_ocr", "-ug",
              is_flag=True,
              default=False,
              help="Use GPU for OCR tasks if available.")
@click.option("--virtual_storage", "-vs",
              is_flag=True,
              default=False,
              help="A boolean variable for checking for virtual storage usage.")
@click.option("--virtual_storage_path", "-vsp",
              default=None,
              help="The location of your virtual storage.")
@click.option("--with_ocr", "-wo",
              is_flag=True,
              default=False,
              help="If there are photos among your files.")
@click.option("--cloud_version", "-cv",
              is_flag=True,
              default=False,
              help="Use cloud API for DeepSeek OCR instead of local model.")
@click.option("--with_deepseek", "-wd",
              is_flag=True,
              default=True,
              help="Use DeepSeek OCR for image text extraction; otherwise EasyOCR.")
@click.option("--model_size", "-ms",
              type=click.Choice(["tiny", "small", "base", "large", "gundam"]),
              default=TINY_TYPE,
              help="Size of the DeepSeek model.")
@click.option("--crop_mode", "-cm",
              is_flag=True,
              default=False,
              help="Split large images into fragments for more detailed recognition.")
@click.option("--base_url", "-bu",
              default="https://api.siliconflow.cn/v1/chat/completions",
              help="API endpoint URL for DeepSeek cloud service.")
@click.option("--api_key_for_deepseek_ocr", "-akd",
              default=None,
              help="API key for DeepSeek cloud service.")
@click.option("--timeout_for_deepseek_ocr", "-tod",
              type=int,
              default=None,
              help="Timeout (seconds) for DeepSeek API requests.")
@click.option("--max_rate_limit_retries", "-mrl",
              type=int,
              default=NUMBER_ATTEMPTS,
              help="Number of retry attempts on rate limit errors.")
@click.option("--prefer_mirror", "-pm",
              is_flag=True,
              default=False,
              help="If True, forces using the mirror endpoint (hf-mirror.com).")
def main(request: str,
         preferences_in_ai: str,
         filter_for_swearing: bool,
         additional_files: tuple,
         models_dir: str,
         with_ai_orchestrator: bool,
         verbose: bool,
         n_ctx: Optional[int],
         n_gpu_layers: int,
         echo: bool,
         max_tokens: int,
         your_token_for_hf: str,
         subdomain: str,
         country: Optional[str],
         protocol: str,
         max_timeout: int,
         is_working: bool,
         type_computer: Optional[str],
         auto_proxies: bool,
         writing_response_to_file: bool,
         your_proxies_dict: tuple,
         determinant_mode: Optional[str],
         accurate_translation: bool,
         your_key_for_deepl: str,
         proprietary_algorithms: bool,
         repo_id: Optional[str],
         filename: Optional[str],
         min_timeout_for_checking_availability: int,
         max_timeout_for_checking_availability: int,
         request_language: str,
         main_prompt_mode: str,
         main_prompt: Optional[str],
         temperature: float,
         retries: int,
         github_proxies: bool,
         url_lst: tuple,
         proxy_retries: Optional[int],
         main_retries: Optional[int],
         lang_lst: tuple,
         use_gpu_for_ocr: bool,
         virtual_storage: bool,
         virtual_storage_path: Optional[str],
         with_ocr: bool,
         cloud_version: bool,
         with_deepseek: bool,
         model_size: str,
         crop_mode: bool,
         base_url: str,
         api_key_for_deepseek_ocr: Optional[str],
         timeout_for_deepseek_ocr: Optional[int],
         max_rate_limit_retries: int,
         prefer_mirror: bool) -> None:
    """
    CLI entry point for AlexRadar.
    Processes the user request with the given options, initializes the
    AlexRadar instance, and prints the generated response.
    """
    banner = """
       █████╗ ██╗     ███████╗██╗  ██╗██████╗  █████╗ ██████╗  █████╗ ██████╗ 
      ██╔══██╗██║     ██╔════╝╚██╗██╔╝██╔══██╗██╔══██╗██╔══██╗██╔══██╗██╔══██╗
      ███████║██║     █████╗   ╚███╔╝ ██████╔╝███████║██║  ██║███████║██████╔╝
      ██╔══██║██║     ██╔══╝   ██╔██╗ ██╔══██╗██╔══██║██║  ██║██╔══██║██╔══██╗
      ██║  ██║███████╗███████╗██╔╝ ██╗██║  ██║██║  ██║██████╔╝██║  ██║██║  ██║
      ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝
        """
    click.echo(banner)

    additional_files_list = list(additional_files) if additional_files else None
    proxies_list = list(your_proxies_dict) if your_proxies_dict else None
    url_list = list(url_lst) if url_lst else None
    lang_lst_list = list(lang_lst) if lang_lst else None
    pref_enum = PreferenceInAI(preferences_in_ai)

    try:
        alex_radar = AlexRadar(
            request=request,
            preferences_in_ai=pref_enum,
            filter_for_swearing=filter_for_swearing,
            additional_files=additional_files_list,
            models_dir=models_dir,
            with_ai_orchestrator=with_ai_orchestrator,
            verbose=verbose,
            n_ctx=n_ctx,
            n_gpu_layers=n_gpu_layers,
            echo=echo,
            max_tokens=max_tokens,
            your_token_for_hf=your_token_for_hf,
            subdomain=subdomain,
            country=country,
            protocol=protocol,
            max_timeout=max_timeout,
            is_working=is_working,
            type_computer=type_computer,
            auto_proxies=auto_proxies,
            writing_response_to_file=writing_response_to_file,
            your_proxies_dict=proxies_list,
            determinant_mode=determinant_mode,
            accurate_translation=accurate_translation,
            your_key_for_deepl=your_key_for_deepl,
            proprietary_algorithms=proprietary_algorithms,
            repo_id=repo_id,
            filename=filename,
            min_timeout_for_checking_availability=min_timeout_for_checking_availability,
            max_timeout_for_checking_availability=max_timeout_for_checking_availability,
            request_language=request_language,
            main_prompt_mode=main_prompt_mode,
            main_prompt=main_prompt,
            temperature=temperature,
            retries=retries,
            github_proxies=github_proxies,
            url_lst=url_list,
            proxy_retries=proxy_retries,
            main_retries=main_retries,
            lang_lst=lang_lst_list,
            use_gpu_for_ocr=use_gpu_for_ocr,
            virtual_storage=virtual_storage,
            virtual_storage_path=virtual_storage_path,
            with_ocr=with_ocr,
            cloud_version=cloud_version,
            with_deepseek=with_deepseek,
            model_size=model_size,
            crop_mode=crop_mode,
            base_url=base_url,
            api_key_for_deepseek_ocr=api_key_for_deepseek_ocr,
            timeout_for_deepseek_ocr=timeout_for_deepseek_ocr,
            max_rate_limit_retries=max_rate_limit_retries,
            prefer_mirror=prefer_mirror
        )
        result = alex_radar.final_ai_request()
        click.echo(result)
    except Exception as e:
        click.echo(f"Error - {e}")
        raise click.Abort()


if __name__ == "__main__":
    main()