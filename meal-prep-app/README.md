# Meal Prep Selector

A full-stack web application for generating randomized meal plans based on protein selections. Built with Vue.js 3 and FastAPI, deployed as a single Docker container.

## Features

- 🍗 Select quantities for different protein types (Chicken, Beef, Pork, Fish, Vegetarian)
- 🎲 Randomly generates meal plans from a recipe database
- 🌐 Scrapes recipe details (ingredients, instructions, images) from cooking websites
- 📱 Responsive design with TailwindCSS
- 🐳 Single Docker container deployment

## Architecture

This is a **monolithic application** where FastAPI serves both the API endpoints and the static Vue.js frontend:

- **Frontend**: Vue.js 3 with Composition API, Vite, and TailwindCSS
- **Backend**: Python 3.11 with FastAPI
- **Scraping**: recipe-scrapers library with wild_mode support
- **Deployment**: Multi-stage Docker build (Node.js → Python)

## Project Structure

```
meal-prep-app/
├── Dockerfile              # Multi-stage build: Node → Python
├── requirements.txt        # Python dependencies
├── app/
│   ├── main.py            # FastAPI app (API + static file serving)
│   ├── scraper.py         # Recipe scraping logic
│   └── data/
│       └── recipes.json   # Recipe database
└── frontend/
    ├── package.json
    ├── vite.config.js
    ├── tailwind.config.js
    ├── index.html
    └── src/
        ├── main.js
        ├── App.vue
        └── components/
            ├── ProteinSelector.vue
            └── RecipeDisplay.vue
```

## Quick Start

### Using Docker (Recommended)

1. **Build the Docker image**:
   ```bash
   cd meal-prep-app
   docker build -t meal-prep-selector .
   ```

2. **Run the container**:
   ```bash
   docker run -p 8000:8000 meal-prep-selector
   ```

3. **Access the application**:
   Open your browser and navigate to `http://localhost:8000`

### Local Development

#### Backend Development

1. **Set up Python environment**:
   ```bash
   cd meal-prep-app
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Run the FastAPI server**:
   ```bash
   cd app
   uvicorn main:app --reload --port 8000
   ```

   The API will be available at `http://localhost:8000/api`

#### Frontend Development

1. **Install dependencies**:
   ```bash
   cd frontend
   npm install
   ```

2. **Run the development server**:
   ```bash
   npm run dev
   ```

   The frontend will be available at `http://localhost:5173` and proxy API requests to `http://localhost:8000`

3. **Build for production**:
   ```bash
   npm run build
   ```

   The built files will be in `frontend/dist/`

## API Endpoints

### `POST /api/generate`

Generate a meal plan based on protein selections.

**Request Body**:
```json
{
  "chicken": 2,
  "beef": 1,
  "pork": 0,
  "fish": 1,
  "vegetarian": 1
}
```

**Response**:
```json
{
  "recipes": [
    {
      "title": "Chicken Parmesan",
      "servings": "4 servings",
      "ingredients": ["chicken", "cheese", "..."],
      "instructions": ["Step 1...", "Step 2..."],
      "image": "https://...",
      "url": "https://..."
    }
  ],
  "total": 5
}
```

### `GET /api/health`

Health check endpoint.

**Response**:
```json
{
  "status": "healthy"
}
```

## Customization

### Adding More Recipes

Edit `app/data/recipes.json` to add more recipe URLs:

```json
{
  "chicken": [
    "https://www.allrecipes.com/recipe/8805/chicken-parmesan/",
    "https://your-new-recipe-url.com"
  ]
}
```

### Styling

The frontend uses TailwindCSS. Modify the components in `frontend/src/components/` to customize the UI.

## Technology Stack

- **Frontend**:
  - Vue.js 3.3 (Composition API)
  - Vite 5.0 (Build tool)
  - TailwindCSS 3.3 (Styling)

- **Backend**:
  - Python 3.11
  - FastAPI 0.104 (Web framework)
  - Uvicorn 0.24 (ASGI server)
  - recipe-scrapers 14.51 (Web scraping)

## License

MIT License
