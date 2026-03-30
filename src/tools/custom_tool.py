from crewai.tools import BaseTool
from pydantic import Field, BaseModel
from typing import Type
from googleapiclient.discovery import build
import os

class YouTubeSearchInput(BaseModel):
    query: str = Field(..., description="The search query string for YouTube videos.")

class YouTubeSearchTool(BaseTool):
    name: str = "YouTube Video Search"
    description: str = (
        "Searches YouTube for videos on a given topic. "
        "Returns a list of video titles, URLs, and channel names. "
        "Input should be a search query string."
    )
    args_schema: Type[BaseModel] = YouTubeSearchInput
    max_results: int = 5 
    def _run(self, query: str) -> str:
        api_key = os.getenv("YOUTUBE_API_KEY")
        if not api_key:
            return "Error: YOUTUBE_API_KEY not found in environment variables."

        youtube = build("youtube", "v3", developerKey=api_key)

        response = youtube.search().list(
            q=query,
            part="snippet",
            type="video",
            maxResults=self.max_results,  
            order="relevance"
        ).execute()

        results = []
        for item in response.get("items", []):
            title = item["snippet"]["title"]
            video_id = item["id"]["videoId"]
            url = f"https://www.youtube.com/watch?v={video_id}"
            channel = item["snippet"]["channelTitle"]
            results.append(f"Title: {title}\nURL: {url}\nChannel: {channel}")

        return "\n\n".join(results) if results else "No videos found."