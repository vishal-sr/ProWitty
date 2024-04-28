import os
from dotenv import load_dotenv
import boto3
import urllib
import json

load_dotenv()

from llama_index.llms.bedrock import Bedrock
def aws_llm():
    llm = Bedrock(
        model = "amazon.titan-text-express-v1",
        aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name = "us-east-1",
    )
    return llm

from llama_index.embeddings.bedrock import BedrockEmbedding
def aws_embed():
    embed = BedrockEmbedding(
        aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name = "us-east-1"
    )

    return embed

import boto3
import os

def get_transcript(video_path):
    # Initialize the Amazon Transcribe client
    transcribe = boto3.client(
        'transcribe',
        aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name = "us-east-1"
    )

    # Upload the video file to an S3 bucket
    bucket_name = 'prowitty-bucket-01'
    s3 = boto3.client(
        's3', 
        aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name = "us-east-1"
    )
    s3.upload_file(video_path, bucket_name, os.path.basename(video_path))

    # Specify the location of the video file in S3
    media_uri = f's3://{bucket_name}/{os.path.basename(video_path)}'

    # Start the transcription job
    response = transcribe.start_transcription_job(
        TranscriptionJobName='TranscriptionJobName01',
        LanguageCode='en-US',  # Specify the language code of the input media
        MediaFormat='mp4',  # Specify the format of the input media
        Media={
            'MediaFileUri': media_uri
        },
        # OutputBucketName=bucket_name,  # Specify the bucket where the transcript will be stored
    )

    # Wait for the transcription job to complete
    while True:
        status = transcribe.get_transcription_job(TranscriptionJobName=response['TranscriptionJob']['TranscriptionJobName'])
        if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
            break

    # Retrieve and return the transcript
    if status['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
        transcript_uri = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
        print(transcript_uri)
        transcript_file = urllib.request.urlopen(transcript_uri)
        transcript_json = json.load(transcript_file)
        return transcript_json['results']['transcripts'][0]['transcript']
    else:
        return None



if __name__ == "__main__":
    # llm = aws_embed()
    # print(llm.get_text_embedding("Bill gates is a"))


    # # Example usage
    # video_file_path = 'path/to/your/video.mp4'
    # transcript = transcribe_video(video_file_path)
    # print(transcript)

    get_transcript(r"C:\Users\vishal\Documents\AI\ProWitty\storage\files\videos\awsAI15316677.autosave.mp4")