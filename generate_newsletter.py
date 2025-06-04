from typing import List, Dict, Any
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NewsletterGenerator:
    def __init__(self):
        """Initialize newsletter generator."""
        pass
    
    def format_date(self, date_str: str) -> str:
        """
        Format date string to a more readable format.
        
        Args:
            date_str: Date string in YYYY-MM-DD format
            
        Returns:
            Formatted date string
        """
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            return date_obj.strftime('%B %d, %Y')
        except ValueError:
            return date_str
    
    def generate_newsletter(self, topic: str, start_date: str, end_date: str, 
                          summary: str, articles: List[Dict[str, Any]]) -> str:
        """
        Generate a formatted newsletter with a single summary and a reference list.
        """
        try:
            formatted_start = self.format_date(start_date)
            formatted_end = self.format_date(end_date)
            newsletter = f"""News Summary: {topic}
Period: {formatted_start} to {formatted_end}
Number of articles: {len(articles)}

Summary:
{summary}

References:
"""
            for i, article in enumerate(articles, 1):
                newsletter += f"{i}. {article['title']}\n   URL: {article['url']}\n"
            return newsletter
        except Exception as e:
            logger.error(f"Error generating newsletter: {str(e)}")
            return "Error generating newsletter"
    
    def save_newsletter(self, newsletter: str, filename: str = None) -> str:
        """
        Save newsletter to a file.
        
        Args:
            newsletter: Newsletter text
            filename: Optional filename, defaults to date-based name
            
        Returns:
            Path to saved file
        """
        try:
            if filename is None:
                filename = f"newsletter_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(newsletter)
            
            return filename
            
        except Exception as e:
            logger.error(f"Error saving newsletter: {str(e)}")
            return None 