# Meal Prep Selector

A single-container monolith application that helps you discover recipes based on the ingredients you want to use.

## Stack

- **Frontend**: Vue 3 with Vite
- **Backend**: FastAPI with Python 3.11
- **Recipe Scraping**: recipe-scrapers library with wild_mode enabled

## Features

- Select the number of recipes you want for different ingredient categories (chicken, beef, pasta, vegetarian)
- Automatically scrapes recipe data from various cooking websites
- Displays recipe details including ingredients, instructions, cooking time, and yields
- Single-container deployment with Docker

## Quick Start

### Build and Run with Docker

```bash
docker build -t meal-prep-selector .
docker run -d -p 8000:8000 meal-prep-selector
```

Then open your browser to `http://localhost:8000`

### API Endpoint

**POST /api/generate**

Request body:
```json
{
  "chicken": 2,
  "beef": 1,
  "pasta": 0,
  "vegetarian": 1
}
```

Response:
```json
{
  "recipes": [
    {
      "title": "Recipe Title",
      "total_time": 45,
      "yields": "4 servings",
      "ingredients": ["ingredient 1", "ingredient 2"],
      "instructions_list": ["step 1", "step 2"],
      "host": "website.com",
      "url": "https://..."
    }
  ]
}
```

## Architecture

The application uses a multi-stage Dockerfile:

1. **Stage 1 (frontend-builder)**: Uses Node 18 to build the Vue frontend with Vite
2. **Stage 2 (python)**: Uses Python 3.11 to run FastAPI with uvicorn, serving both the API and static frontend files

The FastAPI application:
- Mounts `/api` routes for the recipe generation logic
- Mounts `/` to serve the Vue SPA with fallback support
- Randomly selects recipe URLs from `recipes.json` based on ingredient counts
- Scrapes recipes using the `recipe-scrapers` library with `wild_mode=True`
