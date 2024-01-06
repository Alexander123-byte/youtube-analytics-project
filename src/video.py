import os
from googleapiclient.discovery import build


class Video:
    def __init__(self, video_id):
        self.video_id = video_id
        self.api_key = os.environ.get("YT_API_KEY")
        self.youtube = self.get_service()
        self.fetch_video_data()

    @classmethod
    def get_service(cls):
        api_key = os.environ.get("YT_API_KEY")
        return build("youtube", "v3", developerKey=api_key)

    def fetch_video_data(self):
        request = self.youtube.videos().list(
            part="snippet,statistics",
            id=self.video_id
        )
        response = request.execute()

        snippet = response["items"][0]["snippet"]
        statistics = response["items"][0]["statistics"]

        self.title = snippet.get("title", "")
        self.link = f"https://www.youtube.com/watch?v={self.video_id}"
        self.views = int(statistics.get("viewCount", 0))
        self.likes = int(statistics.get("likeCount", 0))

    def __str__(self):
        return self.title


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id

    def fetch_video_data(self):
        super().fetch_video_data()
        self.playlist_id = "PL" + self.video_id
