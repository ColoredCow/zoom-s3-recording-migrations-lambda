import requests, boto3, os, stringcase

class RecordingHandler(object):
    def __init__(self, jsonData):
        self.jsonData = jsonData
        self.s3_bucket = os.environ.get("S3_BUCKET_NAME")
        self.download_token = jsonData["download_token"]
        self.regular_topics = {
            "story_club": "Story Club",
            "town_hall": "Our Townhall",
        }
        self.topic = ""
        self.recording_type = None
        self.recording_types_available = [
            "shared_screen_with_speaker_view",
            "active_speaker",
            "gallery_view"
        ]

    def handle_recording(self):
        recording_start_time_list = []
        
        for index, recording_data in enumerate(self.jsonData["payload"]["object"]["recording_files"]):
            if index == 0:
                recording_start_time_list.append(recording_data["recording_start"])
            elif not recording_data["recording_start"] in recording_start_time_list:
                recording_start_time_list.append(recording_data["recording_start"])
                
        for start_time in recording_start_time_list:
            s3_directory_path = self.get_directory_path() 
            
            for recording_data in self.jsonData["payload"]["object"]["recording_files"]:
                if not recording_data["recording_type"] in self.recording_types_available:
                    continue
            
                self.recording_type = recording_data["recording_type"]
                download_url = recording_data["download_url"] + "?access_token=" + self.download_token 
                file_name = self.get_file_name(recording_data, start_time)
                full_file_path = s3_directory_path + file_name
                self.upload_recording(download_url, full_file_path)
        
        
            
            
    def get_file_name(self, recording_data, recording_time):
        file_extension = recording_data["file_extension"].lower()
        recording_time = recording_data["recording_start"]
        recording_date = recording_data["recording_start"][:10]
        if self.topic in self.regular_topics:
            filename = f"{recording_date}/{recording_time}/{self.topic}_{recording_time}_{self.recording_type}.{file_extension}"
        else:
            topic_name = stringcase.snakecase(self.topic)
            filename = f"{recording_date}/{topic_name}/{recording_time}/{self.topic}_{recording_time}_{self.recording_type}.{file_extension}"
            

        return filename

    def get_directory_path(self):
        s3_file_path = "Zoom-Recordings/Others/"
        
        if self.jsonData["payload"]["object"]["topic"] == self.regular_topics["story_club"]:
            s3_file_path = "Zoom-Recordings/Story-Club/"
            self.topic = "Story_Club"
        elif self.jsonData["payload"]["object"]["topic"] == self.regular_topics["town_hall"]:
            s3_file_path = "Zoom-Recordings/Town-Hall/"
            self.topic = "Town_hall"
        else:
            self.topic = self.jsonData["payload"]["object"]["topic"]
            
        return s3_file_path
    
    def upload_recording(self, download_url, file_path):
        session = requests.Session()
        response = session.get(download_url, stream=True)
        s3_client = boto3.client('s3')
    
        with response as part:
            part.raw.decode_content = True
            conf = boto3.s3.transfer.TransferConfig(multipart_threshold=10000, max_concurrency=4)
            s3_client.upload_fileobj(part.raw, self.s3_bucket, file_path, Config=conf)
    
    def delete_recording_from_zoom(self):
        return
