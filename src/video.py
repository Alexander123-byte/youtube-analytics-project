import os
from googleapiclient.discovery import build


class Video:
    def __init__(self, video_id=None):
        self.video_id = video_id
        self.title = None
        self.like_count = None
        self.fetch_video_data()

    def set_video_id(self, video_id):
        self.video_id = video_id
        self.fetch_video_data()

    @classmethod
    def get_service(cls):
        api_key = os.environ.get("YT_API_KEY")
        return build("youtube", "v3", developerKey=api_key)

    def fetch_video_data(self):
        try:
            if not self.video_id:
                return

            api_key = "YT_API_KEY"
            youtube = build("youtube", "v3", developerKey=api_key)

            video_info = youtube.videos().list(
                part="snippet,statistics",
                id=self.video_id
            ).execute()

            if video_info["items"]:
                snippet = video_info["items"][0]["snippet"]
                statistics = video_info["items"][0]["statistics"]

                self.title = snippet.get("title", None)
                self.like_count = int(statistics.get("likeCount", None))
        except Exception as e:
            print(f"Error fetching video data: {e}")

    def __str__(self):
        return self.title


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id

    def fetch_video_data(self):
        super().fetch_video_data()
        self.playlist_id = "PL" + self.video_id
