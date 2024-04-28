from aws_service import get_transcript
def store():
    pass

def load():
    pass

def S3_loader():
    pass

def write_transcript_file(fileDirectory: str):
    transcript = get_transcript(fileDirectory)
    with open("storage/files/transcript.txt", "a") as file:
        file.write(transcript)


if __name__ == "__main__":
    write_transcript_file(r"C:\Users\vishal\Documents\AI\ProWitty\storage\files\videos\awsAI15316677.autosave.mp4")