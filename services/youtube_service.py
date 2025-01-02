from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from config.settings import Config
import os

class YouTubeService:
    def __init__(self):
        self.api_key = Config.YOUTUBE_API_KEY
        if not self.api_key:
            raise ValueError("YOUTUBE_API_KEY not set in environment variables.")
        self.youtube = build("youtube", "v3", developerKey=self.api_key)


    def get_youtube_comments(self, video_id, part="snippet", max_results=40):
        comments = []
        try:
            response = self.youtube.commentThreads().list(
                part=part,
                videoId=video_id,
                textFormat="plainText",
                maxResults=max_results,
            ).execute()

            while response:
                for item in response.get("items", []):
                    comment_text = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
                    comments.append(comment_text)

                next_page_token = response.get("nextPageToken")
                if not next_page_token:
                    break

                response = self.youtube.commentThreads().list(
                    part=part,
                    videoId=video_id,
                    textFormat="plainText",
                    maxResults=max_results,
                    pageToken=next_page_token,
                ).execute()

        except HttpError as error:
            print(f"An HTTP error occurred: {error.resp.status} - {error.content.decode()}")
            return []
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return []

        return comments
