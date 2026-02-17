from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import json
import random
import logging
from pathlib import Path
from typing import Dict
from scraper import RecipeFetcher

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Protein selection model
class ProteinSelection(BaseModel):
    chicken: int = 0
    beef: int = 0
    pork: int = 0
    fish: int = 0
    vegetarian: int = 0

# Load recipes database
DATA_PATH = Path(__file__).parent / "data" / "recipes.json"

def load_recipes():
    """Load recipes from JSON file"""
    if not DATA_PATH.exists():
        return {}
    with open(DATA_PATH, 'r') as f:
        return json.load(f)

@app.post("/api/generate")
async def generate_meal_plan(selection: ProteinSelection):
    """
    Generate a meal plan based on protein selections.
    Accepts: { "chicken": 2, "beef": 1, ... }
    Returns: List of scraped recipes with ingredients and instructions
    """
    try:
        # Load recipes database
        recipes_db = load_recipes()
        
        # Collect recipe URLs based on selection
        selected_urls = []
        
        for protein, count in selection.dict().items():
            if count > 0 and protein in recipes_db:
                available_recipes = recipes_db[protein]
                # Randomly select 'count' recipes from this protein category
                selected = random.sample(
                    available_recipes, 
                    min(count, len(available_recipes))
                )
                selected_urls.extend(selected)
        
        if not selected_urls:
            return {"recipes": [], "message": "No recipes selected"}
        
        # Scrape recipe details
        fetcher = RecipeFetcher()
        recipes = []
        
        for url in selected_urls:
            try:
                recipe_data = fetcher.fetch_recipe(url)
                recipes.append(recipe_data)
            except Exception as e:
                logger.error(f"Error scraping {url}: {str(e)}")
                # Continue with other recipes even if one fails
                continue
        
        return {"recipes": recipes, "total": len(recipes)}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

# Mount static files - this serves the Vue.js app
# The StaticFiles will serve index.html for routes that don't match files
static_path = Path(__file__).parent / "static"
if static_path.exists():
    app.mount("/", StaticFiles(directory=str(static_path), html=True), name="static")
else:
    logger.warning(f"Static files directory not found at {static_path}")
    
    @app.get("/")
    async def root():
        return {"message": "Frontend not built. Build the Vue app first."}
