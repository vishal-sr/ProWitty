from chat_pipeline import ProWitty
from data_pipeline import DataPipeline
from aws_service import *

def initialize_s3():
    baseLoc = ""
    import boto3

    # Configure AWS credentials and region
    aws_access_key_id = 'YOUR_ACCESS_KEY_ID'
    aws_secret_access_key = 'YOUR_SECRET_ACCESS_KEY'
    aws_region = 'us-west-1'  # Change to your AWS region

    # Create an S3 client
    s3_client = boto3.client('s3', aws_access_key_id=aws_access_key_id,
                            aws_secret_access_key=aws_secret_access_key,
                            region_name=aws_region)

    # Use the S3 client to list objects in a bucket
    response = s3_client.list_objects_v2(Bucket='your-bucket-name')
    print(response)

    return baseLoc

if __name__ == "__main__":
    dp = DataPipeline(
        rawFileStorageDirectory = r"C:\Users\vishal\Documents\AI\ProWitty\storage\files",
        videoFileName = ""
    )
    nodes = dp.build_and_save()

    chat = ProWitty(
        llm = aws_llm(),
        embedModel = aws_embed(),
        dbLoc = "storage/vectorDB",
        collectionName = "defaultDB",
        chatLoc = "storage/chat_store.json"
    )

    print(chat.query("can I get more details on Query execution error in Vector DB ticket?", debug = True))

