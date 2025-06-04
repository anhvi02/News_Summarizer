import openai
from typing import List, Dict, Any
import config
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ArticleSummarizer:
    def __init__(self):
        """Initialize summarizer with OpenAI API key."""
        self.client = openai.OpenAI(api_key=config.OPENAI_API_KEY)
    
    def summarize_corpus(self, articles: List[Dict[str, Any]]) -> str:
        """
        Summarize the combined content of all articles into a focused economic briefing.
        Only includes Australia–Vietnam economic and trade developments.
        
        Args:
            articles: List of article dictionaries
            
        Returns:
            A single summary string formatted as a report
        """
        try:
            # Join article content
            all_content = "\n\n".join([
                f"Title: {a['title']}\nContent: {a.get('content', '')}" for a in articles if a.get('content')
            ])
            if not all_content.strip():
                return "No content to summarize."

            prompt = f"""
    You are an economic analyst writing a focused, concise briefing.

    Summarize the following articles into a structured report on the economic and trade relationship between **Australia and Vietnam**.

    Focus on:
    - Bilateral developments in trade, investment, and regional cooperation
    - Multilateral trade agreements (e.g. CPTPP) if they involve both countries
    - Comments or actions by government officials, diplomats, or trade missions
    - ESG or infrastructure initiatives involving both countries
    - Ignore unrelated geopolitical or regional issues

    Format the summary with the following sections:
    1. **Overview** – 2 to 3 sentences summarizing the big picture
    2. **Key Developments** – bullet points (max 5 items)
    3. **Implications** – what this means for future trade/investment
    4. **Sources** – article titles or brief reference to where the information came from

    Articles:
    {all_content}

    Generate the report below:
    """
            response = self.client.chat.completions.create(
                model=config.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that summarizes news articles concisely."},
                    {"role": "user", "content": prompt}
                ],
                temperature=config.OPENAI_TEMPERATURE,
                max_tokens=600  # You can adjust this based on expected length
            )
            return response.choices[0].message.content.strip()

        except Exception as e:
            logger.error(f"Error summarizing corpus: {str(e)}")
            return "Error generating summary."
