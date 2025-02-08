from pptflow.utils import mylogger

logger = mylogger.get_logger(__name__)


def get_tts_service(tts_service_provider: str):
    # import tts module according to service provider
    if not tts_service_provider:
        logger.error("tts service provider is null")
        raise NotImplementedError(f"tts service provider can't be null")
    logger.info(f"tts service provider: {tts_service_provider}")
    if tts_service_provider.lower() == "azure":
        from .tts_azure import AzureTtsService
        return AzureTtsService()
    elif tts_service_provider.lower() == "edge-tts":
        from .tts_edge_tts import EdgeTtsService
        return EdgeTtsService()
    elif tts_service_provider.lower() == "pyttsx3":
        from pptflow.tts.tts_pyttsx3 import Pyttsx3TtsService
        return Pyttsx3TtsService()
    else:
        logger.error(f"unsupport tts service provider: {tts_service_provider}")
        raise NotImplementedError(f"unsupport tts service provider: {tts_service_provider}")
