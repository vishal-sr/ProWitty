import os
from dotenv import load_dotenv
import boto3

load_dotenv()

def initialize_s3(bucketName: str = ""):

    # Configure AWS credentials and region
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    aws_region = 'us-east-1'

    # Create an S3 client
    s3_client = boto3.client(
        's3', 
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=aws_region
    )

    # Use the S3 client to list objects in a bucket
    baseLoc = f"s3://{bucketName}/"

    return baseLoc

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


def transcribe_video(video_file_path):
    # Initialize the Amazon Transcribe client
    transcribe_client = boto3.client('transcribe')
    
    # Specify the parameters for the transcription job
    job_name = 'transcription-job'
    job_uri = f's3://your-bucket-name/{video_file_path}'
    output_bucket = 'your-output-bucket'
    
    # Start the transcription job
    response = transcribe_client.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': job_uri},
        MediaFormat='mp4',
        OutputBucketName=output_bucket,
        LanguageCode='en-US'  # Change this to the appropriate language code if needed
    )
    
    # Wait for the transcription job to complete
    transcribe_client.get_waiter('transcription_job_completed').wait(
        TranscriptionJobName=job_name
    )
    
    # Get the transcript
    transcript_url = response['TranscriptionJob']['Transcript']['TranscriptFileUri']
    transcript_response = transcribe_client.get_object(Bucket=output_bucket, Key=transcript_url.replace('s3://', ''))
    transcript = transcript_response['Body'].read().decode('utf-8')
    
    return transcript


if __name__ == "__main__":
    llm = aws_embed()
    print(llm.get_text_embedding("Bill gates is a"))


    # Example usage
    video_file_path = 'path/to/your/video.mp4'
    transcript = transcribe_video(video_file_path)
    print(transcript)