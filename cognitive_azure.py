import azure.cognitiveservices.speech as speechsdk


def speech_to_text(filename):
    # Replace with your own subscription key and service region
    speech_key = "53abfd84cacc4a2385d7e711cf3f109f"
    service_region = "westeurope"  # For example, "eastus"

    # Create a speech config object
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

    # Specify the audio file to transcribe
    audio_input = speechsdk.AudioConfig(filename=filename)

    # Create a speech recognizer with audio input
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_input)

    # Perform the speech-to-text transcription
    result = speech_recognizer.recognize_once_async().get()

    # Check the result
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Recognized: {}".format(result.text))
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized")
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))


# Example usage
if __name__ == "__main__":
    # Provide the path to your audio file
    audio_file = "carol.wav"
    speech_to_text(audio_file)