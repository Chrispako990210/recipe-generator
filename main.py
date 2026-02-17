from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from recipe_scrapers import scrape_me
import json
import random
from pathlib import Path
from typing import Dict

app = FastAPI()

# Model for request
class IngredientsRequest(BaseModel):
    chicken: int = 0
    beef: int = 0
    pasta: int = 0
    vegetarian: int = 0

# Load recipes from JSON
RECIPES_FILE = Path(__file__).parent / "recipes.json"
with open(RECIPES_FILE, "r") as f:
    RECIPES_DB = json.load(f)

@app.post("/api/generate")
async def generate_recipes(request: IngredientsRequest):
    """
    Generate recipes based on ingredient counts.
    Accepts a JSON object like {"chicken": 2, "beef": 1, "pasta": 0, "vegetarian": 1}
    Returns scraped recipe data using wild_mode=True.
    """
    selected_urls = []
    
    # Select random URLs based on ingredient counts
    for ingredient, count in request.dict().items():
        if count > 0 and ingredient in RECIPES_DB:
            available_urls = RECIPES_DB[ingredient]
            # Select min(count, available_urls) recipes
            num_to_select = min(count, len(available_urls))
            selected = random.sample(available_urls, num_to_select)
            selected_urls.extend(selected)
    
    if not selected_urls:
        raise HTTPException(status_code=400, detail="No ingredients selected or no recipes available")
    
    # Scrape recipes with wild_mode=True
    recipes = []
    for url in selected_urls:
        try:
            scraper = scrape_me(url, wild_mode=True)
            recipe_data = {
                "title": scraper.title(),
                "total_time": scraper.total_time(),
                "yields": scraper.yields(),
                "ingredients": scraper.ingredients(),
                "instructions": scraper.instructions(),
                "instructions_list": scraper.instructions_list(),
                "host": scraper.host(),
                "url": url
            }
            recipes.append(recipe_data)
        except Exception as e:
            # If scraping fails for one recipe, continue with others
            print(f"Failed to scrape {url}: {str(e)}")
            recipes.append({
                "title": f"Failed to scrape recipe",
                "url": url,
                "error": str(e)
            })
    
    return {"recipes": recipes}

# Mount static files (Vue app) - must be last
static_dir = Path(__file__).parent / "static"
if static_dir.exists():
    app.mount("/", StaticFiles(directory=str(static_dir), html=True), name="static")
else:
    # Fallback for development
    @app.get("/")
    async def read_root():
        return {"message": "Static files not found. Build the frontend first."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
