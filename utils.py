from aws_service import get_transcipt
def store():
    pass

def load():
    pass

def S3_loader():
    pass

def write_transcript_file(fileDirectory: str):
    transcript = get_transcipt(fileDirectory)
    with open("storage/files/transcript.txt") as file:
        file.write(transcript)