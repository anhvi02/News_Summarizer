# News Summarizer

A Python project that fetches, deduplicates, and summarizes news articles on economic, trade, investment, tourism, and diplomatic relations between Australia and Vietnam (or any topic you choose). The project uses NewsAPI and OpenAI's GPT model for summarization.

## Features

- Fetches news articles from NewsAPI
- Supports multiple focused queries for better coverage
- Extracts full article content using newspaper3k
- Deduplicates articles using TF-IDF + cosine similarity or fuzzy string matching
- Summarizes all articles as a single, structured report using OpenAI's GPT model
- Generates a formatted newsletter with the summary and references

## Prerequisites

- Python 3.7+
- NewsAPI API key
- OpenAI API key

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd News_Summarizer
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root with your API keys and input your own key:
```
NEWS_API_KEY=your_newsapi_key
OPENAI_API_KEY=your_openai_key
```

For NewsAPI: https://newsapi.org/  

4. Config how many articles will be extracted for each topic in config.py
```
MAX_ARTICLES_PER_SOURCE = 10
```

## Usage

### Basic CLI Syntax

```bash
python main.py "<topic>" [--start-date YYYY-MM-DD] [--end-date YYYY-MM-DD] [--dedup-method cosine|fuzzy] [--output filename]
```

### Using Multiple Focused Queries (Recommended)

You can specify multiple focused queries for better results:

```bash
python main.py "Vietnam Australia" \
  --queries "Vietnam Australia trade, Vietnam Australia investment, Vietnam Australia tourism, Vietnam Australia agreement" \
  --start-date 2025-06-01 --end-date 2025-06-04 --output aus_vn_summary.txt
```

- `--queries` is a comma-separated list of search queries. The script will fetch, merge, and deduplicate articles from all queries.
- If `--queries` is not provided, the positional `topic` argument is used as a single query.

### Arguments

- `topic`: The main topic to search for news articles (required if --queries is not used)
- `--queries`: Comma-separated list of focused queries (overrides topic)
- `--start-date`: Start date in YYYY-MM-DD format (default: 7 days ago)
- `--end-date`: End date in YYYY-MM-DD format (default: today)
- `--dedup-method`: Deduplication method: 'cosine' or 'fuzzy' (default: 'cosine')
- `--output`: Output filename (default: auto-generated based on timestamp)

## Output Format

The generated newsletter includes:
- Topic and date range
- Number of unique articles
- A single, structured summary (overview, key developments, implications, sources)
- A reference list of article titles and URLs

## Project Structure

- `main.py`: Main script with CLI interface and multi-query support
- `fetch_news.py`: Handles article fetching from NewsAPI
- `deduplicate.py`: Implements article deduplication
- `summarize.py`: Summarizes all articles as a single report using OpenAI
- `generate_newsletter.py`: Formats and saves the newsletter
- `config.py`: Configuration and constants

