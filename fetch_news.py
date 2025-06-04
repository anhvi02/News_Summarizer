from newsapi import NewsApiClient
from newspaper import Article
import config
from typing import List, Dict, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NewsFetcher:
    def __init__(self):
        """Initialize news fetcher with NewsAPI client."""
        self.newsapi = NewsApiClient(api_key=config.NEWS_API_KEY)
    
    def fetch_from_newsapi(self, topic: str, start_date: str, end_date: str) -> List[Dict[str, Any]]:
        """
        Fetch articles from NewsAPI.
        Args:
            topic: Search query
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
        Returns:
            List of article dictionaries
        """
        try:
            response = self.newsapi.get_everything(
                q=topic,
                from_param=start_date,
                to=end_date,
                language=config.NEWS_API_LANGUAGE,
                sort_by=config.NEWS_API_SORT_BY,
                page_size=config.MAX_ARTICLES_PER_SOURCE
            )
            return response['articles']
        except Exception as e:
            logger.error(f"Error fetching from NewsAPI: {str(e)}")
            return []

    def extract_article_content(self, url: str) -> str:
        """
        Extract full article content from URL using newspaper3k.
        Args:
            url: Article URL
        Returns:
            Extracted article text
        """
        try:
            article = Article(url)
            article.download()
            article.parse()
            return article.text
        except Exception as e:
            logger.error(f"Error extracting content from {url}: {str(e)}")
            return ""

    def fetch_all_articles(self, topic: str, start_date: str, end_date: str) -> List[Dict[str, Any]]:
        """
        Fetch articles from NewsAPI and extract their content.
        Args:
            topic: Search query
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
        Returns:
            List of article dictionaries with full content
        """
        articles = []
        newsapi_articles = self.fetch_from_newsapi(topic, start_date, end_date)
        for article in newsapi_articles:
            if article['url']:
                content = self.extract_article_content(article['url'])
                if content:
                    article['content'] = content
                    articles.append(article)
        return articles 