import azure.cognitiveservices.speech as speechsdk
import os
from utils import mylogger

# 创建日志纪录实例
logger = mylogger.get_logger(__name__)


def tts(text, output_audio_filename, setting):
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
