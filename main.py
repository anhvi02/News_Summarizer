import argparse
from datetime import datetime, timedelta
import logging
from fetch_news import NewsFetcher
from deduplicate import ArticleDeduplicator
from summarize import ArticleSummarizer
from generate_newsletter import NewsletterGenerator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def validate_date(date_str: str) -> str:
    """
    Validate date string format.
    
    Args:
        date_str: Date string in YYYY-MM-DD format
        
    Returns:
        Validated date string
        
    Raises:
        ValueError: If date format is invalid
    """
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return date_str
    except ValueError:
        raise ValueError("Date must be in YYYY-MM-DD format")

def main():
    """Main function to run the news summarization pipeline."""
    parser = argparse.ArgumentParser(description='Generate a news summary newsletter')
    parser.add_argument('topic', help='Topic to search for news articles')
    parser.add_argument('--queries', help='Comma-separated list of focused queries (overrides topic)')
    parser.add_argument('--start-date', help='Start date (YYYY-MM-DD)', 
                       default=(datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d'))
    parser.add_argument('--end-date', help='End date (YYYY-MM-DD)',
                       default=datetime.now().strftime('%Y-%m-%d'))
    parser.add_argument('--dedup-method', choices=['cosine', 'fuzzy'],
                       default='cosine', help='Deduplication method')
    parser.add_argument('--output', help='Output filename')
    
    args = parser.parse_args()
    
    try:
        # Validate dates
        start_date = validate_date(args.start_date)
        end_date = validate_date(args.end_date)
        
        logger.info(f"Starting news summarization for topic: {args.topic}")
        logger.info(f"Date range: {start_date} to {end_date}")
        
        # Initialize components
        fetcher = NewsFetcher()
        deduplicator = ArticleDeduplicator(method=args.dedup_method)
        summarizer = ArticleSummarizer()
        newsletter_gen = NewsletterGenerator()
        
        # Determine queries to use
        if args.queries:
            queries = [q.strip() for q in args.queries.split(',') if q.strip()]
        else:
            queries = [args.topic]
        logger.info(f"Using queries: {queries}")
        
        # Fetch and merge articles for all queries
        all_articles = []
        for q in queries:
            logger.info(f"Fetching articles for query: {q}")
            articles = fetcher.fetch_all_articles(q, start_date, end_date)
            logger.info(f"Found {len(articles)} articles for query: {q}")
            all_articles.extend(articles)
        logger.info(f"Total articles before deduplication: {len(all_articles)}")
        
        # Deduplicate articles
        logger.info("Deduplicating articles...")
        unique_articles = deduplicator.deduplicate(all_articles)
        logger.info(f"Found {len(unique_articles)} unique articles after deduplication")
        
        # Summarize the combined content using summarize_corpus
        logger.info("Summarizing all articles as a single corpus...")
        summary = summarizer.summarize_corpus(unique_articles)
        logger.info("Generating newsletter...")
        newsletter = newsletter_gen.generate_newsletter(
            args.topic, start_date, end_date, summary, unique_articles
        )
        output_file = newsletter_gen.save_newsletter(newsletter, args.output)
        if output_file:
            logger.info(f"Newsletter saved to: {output_file}")
        else:
            logger.error("Failed to save newsletter")
        
    except Exception as e:
        logger.error(f"Error in main pipeline: {str(e)}")
        raise

if __name__ == '__main__':
    main() 