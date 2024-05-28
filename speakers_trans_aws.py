import json
import time
import boto3
import requests
from datetime import datetime


def transcribe_file(job_name, file_uri, transcribe_client):
    before = datetime.now()
    transcribe_client.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={"MediaFileUri": file_uri},
        MediaFormat="mp3",
        LanguageCode="he-IL",
        Settings={
            "ShowSpeakerLabels": True,
            "MaxSpeakerLabels": 2
        }
    )

    max_tries = 60
    while max_tries > 0:
        max_tries -= 1
        job = transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
        job_status = job["TranscriptionJob"]["TranscriptionJobStatus"]

        if job_status in ["COMPLETED", "FAILED"]:
            print(f"Job {job_name} is {job_status}.")

            if job_status == "COMPLETED":
                after = datetime.now()
                print(before, after, '===>', after - before)

                transcript_file_uri = job['TranscriptionJob']['Transcript']['TranscriptFileUri']
                download_transcript(transcript_file_uri, job_name + ".json")
            break
        else:
            print(f"Waiting for {job_name}. Current status is {job_status}.")
        time.sleep(10)


def download_transcript(file_uri, local_file_path):
    response = requests.get(file_uri)
    response_json = json.loads(response.content)
    # Extract the speaker labels and transcript from the response
    items = response_json['results']['items']
    speaker_labels = [item['speaker_label'] for item in items if 'speaker_label' in item]
    transcripts = [item['alternatives'][0]['content'] for item in items if 'alternatives' in item]
    # Define a dictionary to map speaker labels to custom names
    speaker_names = {
        "spk_0": "ויטלי",
        "spk_1": "אבא"
    }

    # Combine the speaker labels and transcripts into a single string with custom speaker names
    combined_transcript = ""

    for speaker, transcript in zip(speaker_labels, transcripts):
        speaker_name = speaker_names.get(speaker,
                                         speaker)

        combined_transcript += f"{speaker_name}: {transcript} "

    with open(local_file_path, 'w', encoding='utf-8') as file:
        file.write(combined_transcript.strip())

    print(f"Transcript downloaded to {local_file_path}.")


def main():
    transcribe_client = boto3.client("transcribe",
                                     region_name="eu-central-1"
                                     )
    file_uri = "s3://transcribevitaly/carol.mp3"
    transcribe_file("Transcribe-POC-Speakers-27", file_uri, transcribe_client)


if __name__ == "__main__":
    main()
