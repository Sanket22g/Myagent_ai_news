from pydantic import BaseModel
from typing import List

class RelatedLink(BaseModel):
    label: str
    url: str

class YoutubeVideo(BaseModel):
    title: str
    url: str
    channel_name: str
    publish_date: str
    description: str

class Topic(BaseModel):
    topic_title: str
    category: str
    source: str
    publish_date: str
    article_url: str
    plain_summary: str
    key_takeaways: List[str]
    related_links: List[RelatedLink]
    youtube_videos: List[YoutubeVideo]

class ResearchDigestOutput(BaseModel):
    generated_at: str
    report_title: str
    total_topics: int
    date_range: str
    topics: List[Topic]