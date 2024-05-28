import openai
from datetime import datetime

openai.api_key = "53abfd84cacc4a2385d7e711cf3f109f"
openai.api_base = "https://vitalysregion.openai.azure.com/"
openai.api_type = "azure"
openai.api_version = "2023-09-01-preview"

model_name = "whisper"
deployment_id = "VitalysRegionWhisper"
audio_language = "en"

audio_test_file = r"./carol.wav"

before = datetime.now()
result = openai.Audio.transcribe(
    file=open(audio_test_file, "rb"),
    model=model_name,
    deployment_id=deployment_id
)

after = datetime.now()
print(audio_test_file, '===>', before, after, after - before)
print(result["text"])
