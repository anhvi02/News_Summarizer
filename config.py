import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Keys
NEWS_API_KEY = os.getenv('NEWS_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Constants
MAX_ARTICLES_PER_SOURCE = 10
SIMILARITY_THRESHOLD = 0.8  # For cosine similarity
FUZZY_THRESHOLD = 80  # For fuzzy matching
MAX_SUMMARY_LENGTH = 150  # Maximum words in summary

# NewsAPI settings
NEWS_API_LANGUAGE = 'en'
NEWS_API_SORT_BY = 'relevancy'

# OpenAI settings
OPENAI_MODEL = 'gpt-3.5-turbo'
OPENAI_TEMPERATURE = 0.7 




