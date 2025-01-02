import json
import os
import azure.cognitiveservices.speech as speechsdk
from utils import mylogger
import asyncio
from .setting import Setting

# 创建日志纪录实例
logger = mylogger.get_logger(__name__)


async def tts(text, output_audio_filename, setting):
    """
    Converts the provided text to speech and saves it as an audio file.

    Parameters:
    text (str): The text to be converted to speech.
    output_audio_filename (str): The filename of the output audio file.

    Returns:
    bool: True if the speech synthesis is successful, False otherwise.
    """
    # Initializes the speech configuration using the Azure Speech SDK, obtaining the key and region from environment variables.
    # speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('TTS_AZURE_SPEECH_KEY'),
    #                                        region=os.environ.get('TTS_AZURE_SPEECH_REGION'))
    speech_config = speechsdk.SpeechConfig(subscription=setting.tts_azure_api_key,
                                           region=setting.tts_speech_region)
    # The language of the voice that speaks.
    speech_config.speech_synthesis_voice_name = setting.tts_voice_name
    # Sets the synthesis output format.
    # The full list of supported format can be found here:
    # https://docs.microsoft.com/azure/cognitive-services/speech-service/rest-text-to-speech#audio-outputs
    speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3)
    # Configures the audio output to save to a file.
    file_config = speechsdk.audio.AudioOutputConfig(filename=output_audio_filename)
    # Creates a speech synthesizer instance with the specified configuration.
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=file_config)
    # Asynchronously converts the input text to speech and waits for the operation to complete.
    speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()

    # Checks the result of the speech synthesis.
    if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        # If successful, prints the synthesized text and returns True.
        logger.info("Speech synthesized for text [{}]".format(text))
        return True
    elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
        # If canceled, retrieves the cancellation details.
        cancellation_details = speech_synthesis_result.cancellation_details
        logger.warning("Speech synthesis canceled: {}".format(cancellation_details.reason))
        # If canceled due to an error, prints the error details.
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                logger.error("Error details: {}".format(cancellation_details.error_details))
                logger.error("Did you set the speech resource key and region values?")
        return False


async def list_voices(setting):
    # 初始化 Speech Config
    speech_config = speechsdk.SpeechConfig(subscription=setting.tts_azure_api_key,
                                           region=setting.tts_speech_region)
    # 创建语音列表客户端
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)
    try:
        # 查询可用语音列表
        voices = synthesizer.get_voices_async().get().voices
        # Get the key information
        voice_list = [{"Locale": voice.locale, "Gender": voice.gender.name, "ShortName": voice.short_name,
                       "LocalName": voice.local_name} for voice in voices]
        with open("azure_voice_list.json", "w", encoding="utf-8") as file:
            json.dump(voice_list, file, ensure_ascii=False, indent=4)
            logger.info("Voice list has been saved to azure_voice_list.json")
    except Exception as e:
        logger.error(f"Error occurred: {e}", exc_info=True)
        logger.error("An error occurred while retrieving the voice list. Please check the status of your network.")
        return []


def get_voice_list(setting):
    if not os.path.exists("azure_voice_list.json"):
        asyncio.run(list_voices(setting))
    with open("azure_voice_list.json", "r", encoding="utf-8") as file:
        voice_list = json.load(file)
        logger.info("Voice list has been loaded from azure_voice_list.json")
    return [f'{voice["ShortName"]} ({voice["Locale"]}, {voice["Gender"]})' for voice in voice_list]


if __name__ == '__main__':
    # 初始化 Speech Config
    setting = Setting()
    get_voice_list(setting)

