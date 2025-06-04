from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from fuzzywuzzy import fuzz
import numpy as np
from typing import List, Dict, Any
import config
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ArticleDeduplicator:
    def __init__(self, method: str = 'cosine'):
        """
        Initialize deduplicator with specified method.
        
        Args:
            method: 'cosine' or 'fuzzy' for similarity comparison
        """
        self.method = method
        if method == 'cosine':
            self.vectorizer = TfidfVectorizer(stop_words='english')
    
    def _cosine_similarity(self, articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Deduplicate articles using cosine similarity.
        
        Args:
            articles: List of article dictionaries
            
        Returns:
            List of unique articles
        """
        if not articles:
            return []
            
        # Combine title and content for better comparison
        texts = [f"{article['title']} {article.get('content', '')}" for article in articles]
        
        try:
            # Create TF-IDF matrix
            tfidf_matrix = self.vectorizer.fit_transform(texts)
            
            # Calculate cosine similarity
            similarity_matrix = cosine_similarity(tfidf_matrix)
            
            # Find unique articles
            unique_indices = []
            for i in range(len(articles)):
                is_duplicate = False
                for j in unique_indices:
                    if similarity_matrix[i, j] > config.SIMILARITY_THRESHOLD:
                        is_duplicate = True
                        break
                if not is_duplicate:
                    unique_indices.append(i)
            
            return [articles[i] for i in unique_indices]
            
        except Exception as e:
            logger.error(f"Error in cosine similarity deduplication: {str(e)}")
            return articles
    
    def _fuzzy_similarity(self, articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Deduplicate articles using fuzzy string matching.
        
        Args:
            articles: List of article dictionaries
            
        Returns:
            List of unique articles
        """
        if not articles:
            return []
            
        unique_articles = []
        for article in articles:
            is_duplicate = False
            for unique_article in unique_articles:
                # Compare titles using fuzzy matching
                similarity = fuzz.ratio(article['title'].lower(), 
                                     unique_article['title'].lower())
                if similarity > config.FUZZY_THRESHOLD:
                    is_duplicate = True
                    break
            if not is_duplicate:
                unique_articles.append(article)
        
        return unique_articles
    
    def deduplicate(self, articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Deduplicate articles using the specified method.
        
        Args:
            articles: List of article dictionaries
            
        Returns:
            List of unique articles
        """
        if self.method == 'cosine':
            return self._cosine_similarity(articles)
        else:
            return self._fuzzy_similarity(articles) 