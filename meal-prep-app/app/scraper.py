from recipe_scrapers import scrape_me
from typing import Dict, List, Optional
import logging

# Configure logging
logger = logging.getLogger(__name__)

class RecipeFetcher:
    """
    Recipe scraper using recipe-scrapers library.
    Fetches recipe details from various cooking websites.
    """
    
    def __init__(self):
        """Initialize the recipe fetcher"""
        pass
    
    def fetch_recipe(self, url: str) -> Dict:
        """
        Fetch recipe details from a URL.
        
        Args:
            url: The recipe URL to scrape
            
        Returns:
            Dictionary containing recipe information:
            {
                title: str,
                servings: int,
                ingredients: List[str],
                instructions: List[str],
                image: str,
                url: str
            }
        """
        try:
            # Use recipe-scrapers with wild_mode=True to support more sites
            scraper = scrape_me(url, wild_mode=True)
            
            # Extract recipe data
            recipe_data = {
                "title": self._safe_get(scraper.title),
                "servings": self._safe_get(scraper.yields, default="Not specified"),
                "ingredients": self._safe_get(scraper.ingredients, default=[]),
                "instructions": self._safe_get_instructions(scraper),
                "image": self._safe_get(scraper.image, default=""),
                "url": url
            }
            
            return recipe_data
            
        except Exception as e:
            # Return error information if scraping fails
            return {
                "title": "Failed to fetch recipe",
                "servings": "Unknown",
                "ingredients": [],
                "instructions": [f"Error: {str(e)}"],
                "image": "",
                "url": url,
                "error": str(e)
            }
    
    def _safe_get(self, method_call, default=None):
        """Safely call a method and return default if it fails"""
        try:
            if callable(method_call):
                return method_call()
            return method_call
        except Exception as e:
            logger.debug(f"Failed to extract data: {e}")
            return default
    
    def _safe_get_instructions(self, scraper) -> List[str]:
        """Safely get instructions as a list"""
        try:
            instructions = scraper.instructions()
            if isinstance(instructions, str):
                # Split by newlines and filter empty lines
                return [line.strip() for line in instructions.split('\n') if line.strip()]
            elif isinstance(instructions, list):
                return instructions
            else:
                return [str(instructions)]
        except Exception as e:
            logger.debug(f"Failed to extract instructions: {e}")
            return []
